import pytest

from starbridge import StarbridgeServer


@pytest.mark.asyncio
async def test_add_and_get_note():
    server = StarbridgeServer()
    await server.add_note({"name": "test_note", "content": "This is a test note."})
    notes = await server.get_notes()
    assert any(
        note.text == '{\n  "test_note": "This is a test note."\n}' for note in notes
    )
