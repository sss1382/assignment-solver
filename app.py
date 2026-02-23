from flask import Flask, render_template, request, jsonify
import numpy as np
from scipy.optimize import linear_sum_assignment

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    try:
        matrix_data = request.json['matrix']
        matrix = np.array(matrix_data)
        
        row_ind, col_ind = linear_sum_assignment(matrix)
        total_cost = matrix[row_ind, col_ind].sum()
        
        assignments = []
        for i, j in zip(row_ind, col_ind):
            assignments.append({
                'worker': i + 1,
                'task': j + 1,
                'cost': int(matrix[i, j])
            })
        
        return jsonify({
            'success': True,
            'assignments': assignments,
            'total_cost': int(total_cost)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
