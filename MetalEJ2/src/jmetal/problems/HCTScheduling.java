package jmetal.problems;

import jmetal.core.Problem;
import jmetal.core.Solution;
import jmetal.encodings.solutionType.PermutationAndArrayIntSolutionType;
import jmetal.util.JMException;

public class HCTScheduling extends Problem {

	public HCTScheduling(String solutionType, int cantidad_tareas, int cantidad_maquinas, int cant_estados) {
		
		numberOfVariables_ = 2;
		numberOfObjectives_ = 2;
		numberOfConstraints_ = 0;
		problemName_ = "HCTScheduling";

		upperLimit_ = new double[numberOfVariables_];
		lowerLimit_ = new double[numberOfVariables_];

		length_ = new int[numberOfVariables_];
		//variable 0 es la permutación de tareas
		lowerLimit_[0]	= 0;
		upperLimit_[0]	= cantidad_tareas + cantidad_maquinas -1 -1;
		length_[0]		= cantidad_tareas + (cantidad_maquinas -1); // se supone la posición de la primer máquina
		//variable 1 es el estado en el que se ejecuta cada una de las tareas
		lowerLimit_[1]	= 0;
		upperLimit_[1]	= cant_estados;
		length_[1]		= cantidad_tareas;//un estado definido por cada tarea
		solutionType_ = new PermutationAndArrayIntSolutionType(this);
	}

	@Override
	public void evaluate(Solution solution) throws JMException {
		double [] x = new double[2] ; // 2 decision variables
	    double [] f = new double[2] ; // 2 functions
	    
	    x[0] = solution.getDecisionVariables()[0].getValue();
	    x[1] = solution.getDecisionVariables()[1].getValue();
	    
	    
	    // First function calculo de energía
	    f[0] = 106780.37 * (x[1] + x[2]) + 61704.67 ;
	    // Second function
	    f[1] = 3000 * x[0] ;
	    	    	             
	    solution.setObjective(0,f[0]);    
	    solution.setObjective(1,f[1]);
	    
	}

}
