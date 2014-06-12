package jmetal.encodings.solutionType;

import jmetal.core.Problem;
import jmetal.core.SolutionType;
import jmetal.core.Variable;
import jmetal.encodings.variable.ArrayInt;
import jmetal.encodings.variable.Permutation;

public class PermutationAndArrayIntSolutionType extends SolutionType {
	/**
	 * Constructor
	 * 
	 * @param problem
	 *            Problem being solved
	 */
	public PermutationAndArrayIntSolutionType(Problem problem) {
		super(problem);
	} // Constructor

	/**
	 * Creates the variables of the solution
	 * 
	 * @throws ClassNotFoundException
	 */
	public Variable[] createVariables() throws ClassNotFoundException {
		Variable[] variables = new Variable[2];
		variables[0] = new Permutation(problem_.getLength(0));
		int cantTareas = problem_.getLength(1);
		double [] lower = new double[cantTareas];
		double [] upper = new double[cantTareas];
		for (int i=0; i<cantTareas; i++){
			lower[i] = problem_.getLowerLimit(1);
			upper[i] = problem_.getUpperLimit(1);		}
		variables[1] = new ArrayInt(problem_.getLength(1),lower,upper);
		
		return variables;
	} // createVariables
}
