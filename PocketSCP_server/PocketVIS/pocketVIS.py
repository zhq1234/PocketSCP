from flask import Flask
from pocket_controller.molStarController import molStar
from pocket_controller.parallelController import parallelPlot
from pocket_controller.chordPlotController import chordPlot
from pocket_controller.forcePlotController import forcePlot
from pocket_controller.subpocketController import subPocket
from pocket_controller.singleAxisController import singleAxis

app = Flask(__name__)  # 创建一个实例对象  __name__是必传的参数
app.config["DEBUG"] = True  # 开启debug
app.register_blueprint(chordPlot)
app.register_blueprint(forcePlot)
app.register_blueprint(parallelPlot)
app.register_blueprint(molStar)
app.register_blueprint(subPocket)
app.register_blueprint(singleAxis)


@app.route("/")
def index():
    return {
        "msg": "PocketVIS",
        "success": 200
    }


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, threaded=True)
