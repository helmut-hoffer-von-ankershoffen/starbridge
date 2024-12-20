from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from functools import wraps

import mcp.server.stdio
from mcp import JSONRPCError, JSONRPCRequest, JSONRPCResponse
from mcp.types import JSONRPCMessage, JSONRPCNotification
from opentelemetry import trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import StatusCode

tracer = trace.get_tracer("mcp.server")


class MCPInstrumentor(BaseInstrumentor):
    def instrumentation_dependencies(self):
        return []

    def _instrument(self, **kwargs):
        self._transaction_spans = {}
        original_stdio_server = mcp.server.stdio.stdio_server

        @asynccontextmanager
        @wraps(original_stdio_server)
        async def instrumented_stdio_server(*args, **kwargs):
            async with original_stdio_server(*args, **kwargs) as (
                read_stream,
                write_stream,
            ):
                traced_read = TracedReceiveStream(
                    read_stream, tracer, self._transaction_spans
                )
                traced_write = TracedSendStream(
                    write_stream, tracer, self._transaction_spans
                )
                yield traced_read, traced_write

        mcp.server.stdio.stdio_server = instrumented_stdio_server

    def _uninstrument(self, **kwargs):
        pass


class TracedSendStream:
    def __init__(self, stream, tracer, active_spans):
        self._stream = stream
        self._tracer = tracer
        self._active_spans = active_spans

    async def __aenter__(self):
        await self._stream.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self._stream.__aexit__(exc_type, exc_val, exc_tb)

    async def send(self, msg):
        root = getattr(msg, "root", None)
        txn_span = (
            self._active_spans.get(root.id)
            if root and getattr(root, "id", None) in self._active_spans
            else None
        )

        with self._tracer.start_as_current_span(
            "jsonrpc.response",
            context=trace.set_span_in_context(txn_span) if txn_span else None,
        ) as response_span:
            _set_jsonrpc_span_attributes(response_span, msg)
            try:
                await self._stream.send(msg)
                response_span.set_status(StatusCode.OK)
            except Exception as e:
                response_span.set_status(StatusCode.ERROR, str(e))
                response_span.record_exception(e)
                raise

        # Remove the empty "response" subspan block; end the transaction here if needed
        if txn_span and isinstance(root, JSONRPCResponse | JSONRPCError):
            txn_span.end()
            self._active_spans.pop(root.id, None)

    def __getattr__(self, attr):
        return getattr(self._stream, attr)


class TracedReceiveStream:
    def __init__(self, stream, tracer, active_spans):
        self._stream = stream
        self._tracer = tracer
        self._active_spans = active_spans
        self._current_span = None

    async def __aenter__(self):
        await self._stream.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self._stream.__aexit__(exc_type, exc_val, exc_tb)

    async def receive(self):
        # Manually start a transaction span
        txn_span = self._tracer.start_span(
            "mcp.server.transaction", kind=trace.SpanKind.SERVER
        )
        # Child: jsonrpc.request
        with self._tracer.start_as_current_span(
            "jsonrpc.request", context=trace.set_span_in_context(txn_span)
        ) as request_span:
            msg = await self._stream.receive()
            _set_jsonrpc_span_attributes(request_span, msg)
            request_span.set_status(StatusCode.OK)

        # If request with an ID, store txn_span for the response
        root = getattr(msg, "root", None)
        if isinstance(root, JSONRPCRequest) and root.id is not None:
            self._active_spans[root.id] = txn_span
            with self._tracer.start_as_current_span(
                "request", context=trace.set_span_in_context(txn_span)
            ) as req_span:
                req_span.set_attribute("rpc.method", root.method)
        else:
            # If no ID, we can end now
            txn_span.end()

        return msg

    def __aiter__(self) -> AsyncIterator:
        return TracedAsyncIterator(
            self._stream.__aiter__(), self._tracer, self._active_spans
        )

    def __getattr__(self, attr):
        return getattr(self._stream, attr)


class TracedAsyncIterator:
    def __init__(self, iterator: AsyncIterator, tracer, active_spans):
        self._iterator = iterator
        self._tracer = tracer
        self._active_spans = active_spans

    def __aiter__(self):
        return self

    async def __anext__(self):
        # Manually start a transaction span
        txn_span = self._tracer.start_span(
            "mcp.server.transaction", kind=trace.SpanKind.SERVER
        )
        # Child: jsonrpc.request
        with self._tracer.start_as_current_span(
            "jsonrpc.request", context=trace.set_span_in_context(txn_span)
        ) as request_span:
            msg = await self._iterator.__anext__()
            _set_jsonrpc_span_attributes(request_span, msg)
            request_span.set_status(StatusCode.OK)

        root = getattr(msg, "root", None)
        if isinstance(root, JSONRPCRequest) and root.id is not None:
            self._active_spans[root.id] = txn_span
        else:
            txn_span.end()

        return msg


def _set_jsonrpc_span_attributes(span, msg):
    """Helper to set JSON-RPC span attributes consistently."""
    if not isinstance(msg, JSONRPCMessage):
        return

    root = msg.root
    span.set_attribute("jsonrpc.message", str(msg))

    if isinstance(root, JSONRPCRequest):
        span.set_attribute("jsonrpc.id", root.id)
        span.set_attribute("jsonrpc.type", "request")
        span.set_attribute("jsonrpc.method", root.method)
        if hasattr(root, "params"):
            span.set_attribute("jsonrpc.params", str(root.params))
    elif isinstance(root, JSONRPCNotification):
        span.set_attribute("jsonrpc.type", "notification")
        span.set_attribute("jsonrpc.method", root.method)
    elif isinstance(root, JSONRPCResponse):
        span.set_attribute("jsonrpc.id", root.id)
        span.set_attribute("jsonrpc.type", "response")
        if hasattr(root, "result"):
            span.set_attribute("jsonrpc.result", str(root.result))
    elif isinstance(root, JSONRPCError):
        span.set_attribute("jsonrpc.type", "error")
    else:
        span.set_attribute("jsonrpc.type", "unknown_message_type")
