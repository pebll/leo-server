import json
import shutil
from enum import Enum
from pathlib import Path


class Lang(str, Enum):
    DE = "de"
    EN = "en"


class WebsiteState:
    """Enables having a fix defined scenario order and starting at any of the
    scenarios.

    This keeps the original first scenario index so the state can be reset.
    """

    def __init__(self, first_scn: int, scenarios: dict):
        self.active_scn = first_scn
        self.orig_first_scn = first_scn
        self.scenario_order = [scn["id"] for scn in scenarios]
        self.number_of_scns = len(scenarios)
        self.lang: Lang = Lang.DE
        print(self.scenario_order, "is the order of scns")

    def log_state(self):
        print(
            "WebsiteState: language: {0}, active scenario: {1} ".format(
                self.lang, self.active_scn
            )
        )

    def get_active_scn(self):
        """Return the id of the active scenario."""
        return self.active_scn

    def reset(self):
        """Reset the WebsiteState.

        Reset scenario to first. Reset language to German.
        """
        self.active_scn = self.orig_first_scn
        self.lang = Lang.DE

    def set_next_scenario(self):
        """Set the next scenario as active if it's not the last already."""
        position = self.scenario_order.index(self.active_scn)
        if self.active_scn < self.number_of_scns:
            self.active_scn = self.scenario_order[(position + 1)]
        self.log_state()

    def set_previous_scenario(self):
        """Set the previous scenario as active."""
        position = self.scenario_order.index(self.active_scn)
        if self.active_scn > 0:
            self.active_scn = self.scenario_order[(position - 1)]
        self.log_state()

    def set_language(self, language: str):
        self.lang = [lang for lang in Lang if lang.value == language][0]
        self.log_state()

    def get_language(self):
        return self.lang


class ScenarioViewer:
    """Read paths to JSON files representing scenarios in different
    languages and serve the correct one on request.
    """

    def __init__(
        self,
        scenarios_paths: list[Path] = [
            Path(__file__).parent / "scenarios_de.json"],
    ):
        self.scenario_paths = scenarios_paths

    def _get_scn_by_id(self, scn_id, scenarios) -> dict:
        try:
            referred_scn = [scn for scn in scenarios if scn["id"] == scn_id][0]
        except IndexError as err:
            raise ValueError(
                f"Scenario with index {scn_id} not found in "
                f"{[scn['id'] for scn in scenarios]}"
            ) from err
        return referred_scn

    def _get_scenarios_in_language(self, language: Lang = Lang.DE):
        suffix = language
        path = [
            path
            for path in self.scenario_paths
            if ("_" + suffix + ".json") in path.as_posix()
        ][0]
        with open(path, "r") as file:
            scenarios = json.load(file)

        return scenarios

    def get_scenario_definition(self, scn_id: int, lang: Lang):
        """Return a pure definition of the scenario without leaking user data."""
        scenarios = self._get_scenarios_in_language(lang)
        scenario_definitions = scenarios["scenarios"]
        headings: dict = scenarios["headings"]
        referred_scn = self._get_scn_by_id(scn_id, scenario_definitions)
        referred_scn.update({"headings": headings})
        return referred_scn


class AnswerDB:
    """Manage the answer database JSON file.

    The DB file is similar to a scenario JSON but contains additional user
    answers for corresponding scenarios.
    """

    def __init__(
        self,
        template_db: Path = Path(__file__).parent / "scenarios.json",
        db_file: Path = Path(__file__).parent / ".scenario_answers_db.json",
    ):
        self.template_db = template_db
        self.db_file = db_file
        if not db_file.exists():
            shutil.copy(src=template_db, dst=db_file)

    def _get_scenarios(self):
        with open(self.db_file, "r") as file:
            scenarios = json.load(file)["scenarios"]

        return scenarios

    def _get_scn_by_id(self, scn_id, scenarios):
        try:
            referred_scn = [scn for scn in scenarios if scn["id"] == scn_id][0]
        except IndexError as err:
            raise ValueError(
                f"Scenario with index {scn_id} not found in "
                f"{[scn['id'] for scn in scenarios]}"
            ) from err
        return referred_scn

    def store_answer(self, scn_id, decision, conseqs, user_uid):
        """Load the DB, add a new answer and persist it back to disk."""
        scenarios = self._get_scenarios()
        referred_scn = self._get_scn_by_id(scn_id, scenarios)

        new_answer = {
            "decision": decision,
            "conseqs": conseqs,
            "user_uid": user_uid,
        }
        referred_scn["answers"].append(new_answer)
        with open(self.db_file, "w") as file:
            scenarios_dict = {"scenarios": scenarios}
            json.dump(scenarios_dict, file, ensure_ascii=False, indent=4)

        print(
            f"Stored new answer in the database at (following path might be in a "
            f"container!): {self.db_file.as_posix()}"
        )


if __name__ == "__main__":
    with open(Path(__file__).parent.parent / "scenarios_de.json") as file:
        scns = json.load(file)["scenarios"]
        state = WebsiteState(0, scns)
        state.set_language("en")
