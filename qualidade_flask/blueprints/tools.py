from flask import Blueprint, render_template

tools = Blueprint('tools', __name__)

@tools.route('/pareto')
def pareto(): return render_template('pareto.html')

@tools.route('/ishikawa')
def ishikawa(): return render_template('ishikawa.html')

@tools.route('/5w2h')
def ferramenta_5w2h(): return render_template('5w2h.html')

@tools.route('/cep')
def cep(): return render_template('cep.html')

@tools.route('/histograma')
def histograma(): return render_template('histograma.html')

@tools.route('/dispersao')
def dispersao(): return render_template('dispersao.html')
