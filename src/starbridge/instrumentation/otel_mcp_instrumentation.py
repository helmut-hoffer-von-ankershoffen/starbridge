"""OpenTelemetry instrumentation for MCP protocol."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from functools import wraps
from types import TracebackType
from typing import Any, Never, Self

import mcp.server.stdio
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream
from mcp import JSONRPCError, JSONRPCRequest, JSONRPCResponse
from mcp.types import JSONRPCMessage, JSONRPCNotification
from opentelemetry import trace
from opentelemetry.instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.trace import Span, StatusCode, Tracer

tracer = trace.get_tracer("mcp.server")


class MCPInstrumentor(BaseInstrumentor):  # pragma: no cover
    """Instrumentor for MCP protocol communications."""

    def instrumentation_dependencies(self) -> list:  # noqa: PLR6301
        """
        Get instrumentation dependencies.

        Returns:
            list: List of required dependencies

        """
        return []

    def _instrument(self, **_kwargs) -> None:
        """
        Install instrumentation.

        Args:
            **kwargs: Instrumentation options

        """
        self._transaction_spans = {}
        original_stdio_server = mcp.server.stdio.stdio_server

        @asynccontextmanager
        @wraps(original_stdio_server)
        async def instrumented_stdio_server(
            *args, **kwargs
        ) -> AsyncIterator[tuple[TracedReceiveStream, TracedSendStream]]:
            async with original_stdio_server(*args, **kwargs) as (
                read_stream,
                write_stream,
            ):
                traced_read = TracedReceiveStream(
                    read_stream,
                    tracer,
                    self._transaction_spans,
                )
                traced_write = TracedSendStream(
                    write_stream,
                    tracer,
                    self._transaction_spans,
                )
                yield traced_read, traced_write

        mcp.server.stdio.stdio_server = instrumented_stdio_server

    def _uninstrument(self, **_kwargs) -> Never:
        """
        Uninstall instrumentation.

        Args:
            **kwargs: Uninstallation options

        Raises:
            NotImplementedError: Uninstallation is not supported

        """
        msg = "Uninstrumentation not supported"
        raise NotImplementedError(msg)


def _handle_transaction(tracer: Tracer, msg: JSONRPCMessage, span_kind: str, active_spans: dict[str, Span]) -> None:
    """Handle span lifecycle for a JSON-RPC request/response transaction.

    Args:
        tracer (Tracer): OpenTelemetry tracer
        msg (JSONRPCMessage): Message to handle
        span_kind (str): Span kind
        active_spans (dict[str, Span]): Dictionary of active spans by message ID
    """
    root = msg.root
    msg_id: str = getattr(root, "id", None) or ""

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


def _handle_notification(tracer: Tracer, msg: JSONRPCNotification, span_kind: str) -> None:
    """Handle span for a JSON-RPC notification.

    Args:
        tracer (Tracer): OpenTelemetry tracer
        msg (JSONRPCMessage): Message to handle
        span_kind (str): Span kind
    """
    with tracer.start_span(
        f"mcp.{span_kind.lower()}.notification.{msg.method}",
        kind=getattr(trace.SpanKind, span_kind.upper()),
    ) as span:
        if isinstance(msg, JSONRPCNotification):
            span.set_attribute("jsonrpc.notification.method", msg.method)
            if hasattr(msg, "params"):
                span.set_attribute("jsonrpc.notification.params", str(msg.params))
            span.set_status(StatusCode.OK)


def _set_request_attributes(span: Span, msg: JSONRPCMessage) -> None:
    """Set span attributes for a JSON-RPC request.

    Args:
        span (Span): Span to set attributes on
        msg (JSONRPCMessage): Message to set attributes from
    """
    root = msg.root
    if isinstance(root, JSONRPCRequest):
        span.set_attribute("jsonrpc.request.id", root.id)
        span.set_attribute("jsonrpc.request.method", root.method)
        if hasattr(root, "params"):
            span.set_attribute("jsonrpc.request.params", str(root.params))


def _set_response_attributes(span: Span, msg: JSONRPCMessage) -> None:
    """Set span attributes for a JSON-RPC response.

    Args:
        span (Span): Span to set attributes on
        msg: Message to set attributes from
    """
    root = msg.root
    if isinstance(root, JSONRPCResponse):
        span.set_attribute("jsonrpc.response.result", str(root.result))
        span.set_status(StatusCode.OK)
    elif isinstance(root, JSONRPCError):
        span.set_attribute("jsonrpc.error.code", root.error.code)
        span.set_attribute("jsonrpc.error.message", root.error.message)
        span.set_status(StatusCode.ERROR, root.error.message)


class TracedSendStream:
    """Stream wrapper that traces outgoing messages."""

    def __init__(self, stream: MemoryObjectSendStream, tracer: Tracer, active_spans: dict[str, Span]) -> None:
        """
        Initialize traced send stream.

        Args:
            stream (MemoryObjectSendStream): Stream to wrap
            tracer (Tracer): OpenTelemetry tracer
            active_spans (dict[str, Span]): Dictionary of active spans by message ID

        """
        self._stream = stream
        self._tracer = tracer
        self._active_spans = active_spans

    async def __aenter__(self) -> Self:
        """
        Enter the async context manager.

        Returns:
            Self: The traced send stream instance.
        """
        await self._stream.__aenter__()
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        """
        Exit the async context manager.

        Args:
            exc_type (type[BaseException] | None): Exception type
            exc_val (BaseException | None): Exception value
            exc_tb (TracebackType | None): Traceback

        """
        await self._stream.__aexit__(exc_type, exc_val, exc_tb)

    async def send(self, msg: JSONRPCMessage) -> None:
        """
        Send a message with tracing.

        Args:
            msg (JSONRPCMessage): Message to send

        """
        root = getattr(msg, "root", None)
        if isinstance(root, JSONRPCNotification):
            _handle_notification(
                self._tracer,
                root,
                "CLIENT",
            )  # We're sending a notification
        else:
            _handle_transaction(
                self._tracer,
                msg,
                "CLIENT",
                self._active_spans,
            )  # We're sending a request/response

        await self._stream.send(msg)

    def __getattr__(self, attr: str) -> type[Any]:
        """
        Get an attribute from the underlying stream.

        Args:
            attr (str): Name of the attribute to get.

        Returns:
            type[Any]: The attribute value from the underlying stream.
        """
        return getattr(self._stream, attr)


class TracedReceiveStream:
    """Stream wrapper that traces incoming messages."""

    def __init__(self, stream: MemoryObjectReceiveStream, tracer: Tracer, active_spans: dict[str, Span]) -> None:
        """
        Initialize traced receive stream.

        Args:
            stream (MemoryObjectReceiveStream): Stream to wrap
            tracer (Tracer): OpenTelemetry tracer
            active_spans (dict[str,Span]): Dictionary of active spans by message ID

        """
        self._stream = stream
        self._tracer = tracer
        self._active_spans = active_spans
        self._current_span = None

    async def __aenter__(self) -> Self:
        """
        Enter the async context manager.

        Returns:
            Self: The traced receive stream instance.
        """
        await self._stream.__aenter__()
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        """
        Exit the async context manager.

        Args:
            exc_type (type[BaseException] | None): Exception type
            exc_val (BaseException | None): Exception value
            exc_tb (TracebackType | None): Traceback

        """
        await self._stream.__aexit__(exc_type, exc_val, exc_tb)

    async def receive(self) -> JSONRPCMessage | JSONRPCNotification | None:
        """
        Receive a message with tracing.

        Returns:
            JSONRPCMessage: The received message

        """
        msg: JSONRPCMessage = await self._stream.receive()
        root = getattr(msg, "root", None)

        if isinstance(root, JSONRPCNotification):
            _handle_notification(
                self._tracer,
                root,
                "SERVER",
            )  # It's an incoming notification
        else:
            _handle_transaction(
                self._tracer,
                msg,
                "SERVER",
                self._active_spans,
            )  # It's an incoming request/response

        return msg

    def __aiter__(self) -> AsyncIterator:
        """
        Return async iterator for the traced receive stream.

        Returns:
            AsyncIterator: Traced async iterator for receiving messages.

        """
        return TracedAsyncIterator(
            self._stream.__aiter__(),
            self._tracer,
            self._active_spans,
        )

    def __getattr__(self, attr: str) -> type[Any]:
        """
        Get an attribute from the underlying stream.

        Args:
            attr (str): Name of the attribute to get.

        Returns:
            type[Any]: The attribute value from the underlying stream.
        """
        return getattr(self._stream, attr)


class TracedAsyncIterator:
    """Async iterator wrapper that traces message iteration."""

    def __init__(self, iterator: AsyncIterator, tracer: Tracer, active_spans: dict[str, Span]) -> None:
        """
        Initialize traced async iterator.

        Args:
            iterator (AsyncIterator): Iterator to wrap
            tracer (Tracer): OpenTelemetry tracer
            active_spans (dict[str,Span]): Dictionary of active spans by message ID

        """
        self._iterator = iterator
        self._tracer = tracer
        self._active_spans = active_spans

    def __aiter__(self) -> Self:
        """
        Return the async iterator instance.

        Returns:
            Self: The traced async iterator instance.

        """
        return self

    async def __anext__(self) -> JSONRPCMessage:
        """
        Get next message from the iterator with tracing.

        Returns:
            JSONRPCMessage: The next message from the iterator.

        Raises:
            StopAsyncIteration: When there are no more items to iterate over.

        """
        msg = await self._iterator.__anext__()
        root = getattr(msg, "root", None)

        if isinstance(root, JSONRPCNotification):
            _handle_notification(self._tracer, root, "CLIENT")
        else:
            _handle_transaction(self._tracer, msg, "SERVER", self._active_spans)

        return msg
