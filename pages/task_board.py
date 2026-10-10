from playwright.sync_api import Page


class TaskBoardPage:
    """User-facing actions and semantic locators for the task board."""

    def __init__(self, page: Page):
        self.page = page
        self.new_task = page.get_by_role("textbox", name="New task")
        self.add_button = page.get_by_role("button", name="Add task", exact=True)
        self.tasks = page.get_by_role("list", name="Tasks")
        self.remaining = page.get_by_role("status")
        self.error = page.get_by_role("alert")

    def open(self, base_url: str):
        self.page.goto(base_url)
        return self

    def add(self, description: str):
        self.new_task.fill(description)
        self.add_button.click()

    def task(self, description: str):
        return self.tasks.get_by_role("checkbox", name=description, exact=True)

    def complete(self, description: str):
        self.task(description).check()

    def delete(self, description: str):
        self.tasks.get_by_role("button", name=f"Delete {description}", exact=True).click()
