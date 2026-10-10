import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
def test_add_task(board):
    board.add("Review release evidence")
    expect(board.task("Review release evidence")).to_be_visible()
    expect(board.task("Review release evidence")).not_to_be_checked()
    expect(board.remaining).to_have_text("1 tasks remaining")


def test_complete_and_reopen_task(board):
    board.add("Run acceptance checks")
    board.complete("Run acceptance checks")
    expect(board.remaining).to_have_text("0 tasks remaining")
    board.task("Run acceptance checks").uncheck()
    expect(board.remaining).to_have_text("1 tasks remaining")


@pytest.mark.parametrize("description", ["", "   "])
def test_reject_blank_task(board, description):
    board.add(description)
    expect(board.error).to_have_text("Enter a task")
    expect(board.tasks.get_by_role("listitem")).to_have_count(0)


def test_delete_only_selected_task(board):
    board.add("Keep this task")
    board.add("Remove this task")
    board.delete("Remove this task")
    expect(board.task("Remove this task")).to_have_count(0)
    expect(board.task("Keep this task")).to_be_visible()
    expect(board.remaining).to_have_text("1 tasks remaining")


def test_new_context_starts_empty(board):
    expect(board.tasks.get_by_role("listitem")).to_have_count(0)
    expect(board.remaining).to_have_text("0 tasks remaining")
