# main.py
from fastapi import FastAPI
from fastapi import Form, Query
from fastapi.staticfiles import StaticFiles
import uvicorn
from utils import AnswerDB, WebsiteState, ScenarioViewer
from pathlib import Path
import json
from pydantic import BaseModel
import uuid

root_dir = Path(__file__).parent.parent
static_content_path = root_dir / "static"


class LangRequest(BaseModel):
    lang: str


db = AnswerDB(
    template_db=root_dir / "scenarios_de.json", db_file=root_dir / ".database.json"
)

with open(root_dir / "scenarios_de.json") as file:
    scenario_list = json.load(file)["scenarios"]
state = WebsiteState(0, scenarios=scenario_list)


scn_viewer = ScenarioViewer(
    scenarios_paths=[
        root_dir / "scenarios_de.json",
        root_dir / "scenarios_en.json",
    ],
)

app = FastAPI(title="Survey-Game API")
app.mount("/static", StaticFiles(directory=static_content_path), name="static")


@app.get(
    "/get-session-id", summary="Request a new session and session id from backend."
)
def get_session_id():
    """
    Request a new session and session id from backend.

    Backend will generate a new unique universal ID for this session.
    That way the user can be identified in an anonymous way.

    **Note**:
    * The Server does only support one client at a time currently.
    """
    session_id = uuid.uuid4()
    return {
        "msg": "Started a new Session! Supply this session id again when sending user input to the backend.",
        "session_id": session_id,
    }


@app.get("/set-lang", summary="Sets the Language to German ('de') or english ('en')")
def set_lang(language: str = Query(...)):
    """
    **Sets Language to German ('de') or english ('en')**

    Alter the WebsiteState such that the language is the specified language.

    **Note**:
    * WebsiteState consists of language and scenario id by the way.
    * In Future version it should consist of language, scenario_id, page_id and possibly a session_id
    * the session_id could be a renaming and actual use of the user_uuid that already needs to be provided
      when submitting data.
    """
    state.set_language(language)
    return {"msg": f"set language to a {language}"}


@app.post(
    "/get-scenario",
    summary="Endpoint where the client can fetch what to display in the current WebsiteState. ",
)
def get_scenario():
    """
    **Endpoint where the client can fetch what to display in the current WebsiteState.**
    * current WebsiteState will be determined
    * according Data for the client to display in this state will be sent back.
    """
    lang = state.get_language()
    scn_id = state.get_active_scn()
    definition = scn_viewer.get_scenario_definition(
        scn_id=scn_id,
        lang=lang,
    )

    return {
        "message": f"Scenario definition {scn_id} was retrieved in lang {lang} from database.",
        "definition": definition,
    }


@app.get("/reset", summary="Switch WebsiteState to the first scenario.")
def reset():
    """
    **Switch WebsiteState to the first scenario and language to german.**

    **Notes**:
    * Does not yet return any Scenario Data to display on the client. Use get-scenario for this!
    * In this version Scenarios are still sequentially ordered and only have one page
      but his could change in the future!

    **Known Bugs**:
    * sometimes the button calling this API needs to be pressed two times before it switches the scenario.
    * This was probably more a deception due to bad frontend not showing if button was clicked.

    """
    state.reset()
    return {"active_scn": state.get_active_scn()}


@app.get("/next-scenario", summary="Switch WebsiteState to the next scenario.")
def next_scenario():
    """
    **Switch WebsiteState to the next scenario.**

    **Notes**:
    * Does not yet return any Scenario Data to display on the client. Use get-scenario for this!
    * In this version Scenarios are still sequentially ordered and only have one page
      but his could change in the future!

    **Known Bugs**:
    * sometimes the button calling this API needs to be pressed two times before it switches the scenario.
    * This was probably more a deception due to bad frontend not showing if button was clicked.

    """
    state.set_next_scenario()
    return {"active_scn": state.get_active_scn()}


@app.get("/prev-scenario", summary="Switch WebsiteState to the previous scenario.")
def prev_scenario():
    """
    **Switch WebsiteState to the previous scenario.**
    **Notes**:
    * In the current implementation of browser client there is **no back button** and hence this endpoint is usually not used.
    * Does not yet return any Scenario Data to display on the client. Use get-scenario for this!
    * In this version Scenarios are still sequentially ordered and only have one page
      but his could change in the future!

    **Known Bugs**:
    * sometimes the button calling this API needs to be pressed two times before it switches the scenario.
      This might be an Error in WebsiteState class.

    """
    state.set_previous_scenario()
    return {"active_scn": state.get_active_scn()}


@app.post(
    "/submit",
    summary=";Endpoint for the client to send in newly obtained form data.",
)
def submit(choice: str = Form(...), conseqs: str = Form(...), uuid: str = Form(...)):
    """
    **Endpoint for the client to send in newly obtained form data.**

    The form data should contain
    * a free text input called "conseqs" containing what the user thinks could be
      consequences of his/her decision.
    * a choice='choice1'|'choice2' any other string is interpreted as choice2
    * a user uuid (so far in the browser client this yet only a mocked ID)

    **Note:**
    * upon receival of the form data after storing the answer in the JSON Database a message will be returned by the endpoint.
    * the return message is not shown in the current implementation of the browser client.
    """
    print("Survey Data POST from Client was received.")
    choice1 = choice == "choice1"
    msg = db.store_answer(
        conseqs=conseqs,
        decision="1" if choice == "choice1" else "2",
        scn_id=state.get_active_scn(),
        user_uid=uuid,
    )
    return {
        "submitted_data": {"choice1": choice1, "consequences": conseqs, "uuid": uuid},
        "db_response": msg,
    }


@app.get("/hello", summary="A proof of concept API endpoint for debugging.")
def hello():
    return {"message": "Hello from FastAPI!"}


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
