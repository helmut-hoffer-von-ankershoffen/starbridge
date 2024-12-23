from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from functools import wraps

import mcp.server.stdio
from mcp import JSONRPCError, JSONRPCRequest, JSONRPCResponse
from mcp.types import JSONRPCNotification
from opentelemetry import trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import StatusCode

tracer = trace.get_tracer("mcp.server")


class MCPInstrumentor(BaseInstrumentor):  # pragma: no cover
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
        raise NotImplementedError("Uninstrumentation not supported")


def _handle_transaction(tracer, msg, span_kind, active_spans):
    """Handle span lifecycle for a JSON-RPC request/response transaction"""
    root = msg.root
    msg_id = getattr(root, "id", None)

    if isinstance(root, JSONRPCRequest):
        # Start new transaction span
        span = tracer.start_span(
            f"mcp.{span_kind.lower()}.transaction.{root.method}",
            kind=getattr(trace.SpanKind, span_kind.upper()),
        )
        _set_request_attributes(span, msg)
        active_spans[msg_id] = span
    elif isinstance(root, JSONRPCResponse | JSONRPCError):
        # End existing transaction span
        span = active_spans.pop(msg_id, None)
        if span:
            _set_response_attributes(span, msg)
            span.end()


def _handle_notification(tracer, msg, span_kind):
    """Handle span for a JSON-RPC notification"""
    with tracer.start_span(
        f"mcp.{span_kind.lower()}.notification.{msg.root.method}",
        kind=getattr(trace.SpanKind, span_kind.upper()),
    ) as span:
        if isinstance(msg.root, JSONRPCNotification):
            span.set_attribute("jsonrpc.notification.method", msg.root.method)
            if hasattr(msg.root, "params"):
                span.set_attribute("jsonrpc.notification.params", str(msg.root.params))
            span.set_status(StatusCode.OK)


def _set_request_attributes(span, msg):
    """Set span attributes for a JSON-RPC request"""
    root = msg.root
    if isinstance(root, JSONRPCRequest):
        span.set_attribute("jsonrpc.request.id", root.id)
        span.set_attribute("jsonrpc.request.method", root.method)
        if hasattr(root, "params"):
            span.set_attribute("jsonrpc.request.params", str(root.params))


def _set_response_attributes(span, msg):
    """Set span attributes for a JSON-RPC response"""
    root = msg.root
    if isinstance(root, JSONRPCResponse):
        span.set_attribute("jsonrpc.response.result", str(root.result))
        span.set_status(StatusCode.OK)
    elif isinstance(root, JSONRPCError):
        span.set_attribute("jsonrpc.error.code", root.error.code)
        span.set_attribute("jsonrpc.error.message", root.error.message)
        span.set_status(StatusCode.ERROR, root.error.message)


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

        if isinstance(root, JSONRPCNotification):
            _handle_notification(
                self._tracer, msg, "CLIENT"
            )  # We're sending a notification
        else:
            _handle_transaction(
                self._tracer, msg, "CLIENT", self._active_spans
            )  # We're sending a request/response

        await self._stream.send(msg)

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
        msg = await self._stream.receive()
        root = getattr(msg, "root", None)

        if isinstance(root, JSONRPCNotification):
            _handle_notification(
                self._tracer, msg, "SERVER"
            )  # It's an incoming notification
        else:
            _handle_transaction(
                self._tracer, msg, "SERVER", self._active_spans
            )  # It's an incoming request/response

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
        msg = await self._iterator.__anext__()
        root = getattr(msg, "root", None)

        if isinstance(root, JSONRPCNotification):
            _handle_notification(self._tracer, msg, "CLIENT")
        else:
            _handle_transaction(self._tracer, msg, "SERVER", self._active_spans)

        return msg
