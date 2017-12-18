import sys
import core
import state


class StartUp(state.State): pass


config = {
    "screen_size": (1024, 768),
    "bgcolor": (150, 150, 150)
}
if __name__ == "__main__":
    startup = StartUp()
    app = core.App(config=config)
    sys.exit(app.run_with_state(startup))
