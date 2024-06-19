from typing import Optional
from pydantic import BaseModel

from pydantic import Field

from .base_class import BaseAction, BaseResponse

from composio.local_tools.local_workspace.commons.get_logger import get_logger
from composio.local_tools.local_workspace.commons.history_processor import (
    history_recorder,
)
from composio.local_tools.local_workspace.commons.local_docker_workspace import (
    communicate,
)

logger = get_logger()


class LinterRequest(BaseModel):
    workspace_id: str = Field(..., description="workspace-id for the linter to work")

class LinterResponse(BaseModel):
    lint_errors: str = Field(..., description="list of lint errors")


class PylintLinter(BaseAction):
    _display_name = "Lint Python code with Pylint"
    _request_schema = LinterRequest
    _response_schema = LinterResponse

    @history_recorder()
    def execute(self, request_data: LinterRequest, authorisation_data: dict = {}) -> BaseResponse:
        self._setup(request_data)
        cmd = "tox -e pylint"
        pylint_out, return_code = communicate(self.container_process, self.container_obj, cmd, self.parent_pids, timeout_duration=200)
        if return_code == 0:
            pylint_out = f"No errors detected by pylint. pylint output: {pylint_out}"
        return BaseResponse(output=pylint_out, return_code=return_code)

class Flake8Linter(BaseAction):
    _display_name = "Lint Python code with Flake8"
    _request_schema = LinterRequest
    _response_schema = LinterResponse

    @history_recorder()
    def execute(self, request_data: LinterRequest, authorisation_data: dict = {}) -> BaseResponse:
        self._setup(request_data)
        cmd = "tox -e flake8"
        flake8_out, return_code = communicate(self.container_process, self.container_obj, cmd, self.parent_pids, timeout_duration=70)
        if return_code == 0:
            flake8_out = f"No errors detected by Flake8. tox output: {flake8_out}"
        return BaseResponse(output=flake8_out, return_code=return_code)


class BlackLinter(BaseAction):
    _display_name = "Format Python code with Black"
    _request_schema = LinterRequest
    _response_schema = LinterResponse

    @history_recorder()
    def execute(self, request_data: LinterRequest, authorisation_data: dict = {}) -> BaseResponse:
        self._setup(request_data)
        cmd = "tox -e black"
        black_output, return_code =  communicate(self.container_process, self.container_obj, cmd, self.parent_pids, timeout_duration=45)
        if return_code == 0:
            black_output = f"No errors detected by black. tox output: {black_output}"
        return BaseResponse(output=black_output, return_code=return_code)


class IsortLinter(BaseAction):
    _display_name = "Sort imports in Python code with Isort"
    _request_schema = LinterRequest
    _response_schema = LinterResponse

    @history_recorder()
    def execute(self, request_data: LinterRequest, authorisation_data: dict = {}) -> BaseResponse:
        self._setup(request_data)
        cmd = "tox -e isort"
        isort_out, return_code = communicate(self.container_process, self.container_obj, cmd, self.parent_pids, timeout_duration=45)
        if return_code == 0:
            isort_out = f"No errors detected by isort. tox output: {isort_out}"
        return BaseResponse(output=isort_out, return_code=return_code)



