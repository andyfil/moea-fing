package jmetal.operators.crossover;

import jmetal.core.Operator;
import jmetal.core.Problem;
import jmetal.core.Solution;
import jmetal.core.Variable;
import jmetal.util.JMException;

public class GralCrossover {
	private Problem _problem;
	
	public Object crucePermutation(SinglePointTwoPointCrossover crossoverPerm, Problem problem_, Solution [] parents){
		
		Variable [] var1 = parents[0].getDecisionVariables() ; 
		Variable [] var2 = parents[1].getDecisionVariables() ;
		
		Variable [] varPerm1 = new Variable[1];
		Variable [] varPerm2 = new Variable[1];
		varPerm1[0] = var1[0]; // Permutation 1
		varPerm2[0] = var2[0]; // Permutation 2
		Solution [] solPermAux = new Solution[2];
		
		solPermAux[0] = new Solution(problem_,varPerm1);  
		solPermAux[1] = new Solution(problem_,varPerm2);  
		
		double prob = (double) crossoverPerm.getParameter("probability");
		//Solution[] offspring  = crossoverPerm.doCrossover(prob, solPermAux[0], solPermAux[1]);
		//return offspring;
		return null;
	}
	public Object cruceArrayInt(SinglePointCrossover crossoverArray, Problem problem_, Solution [] parents) throws JMException{
		
		Variable [] var1 = parents[0].getDecisionVariables() ; 
	 	Variable [] var2 = parents[1].getDecisionVariables() ;
	 	
	 	Variable [] varArray1 = new Variable[1];
	 	Variable [] varArray2 = new Variable[1];
	 	varArray1[0] = var1[1]; // Array 1
	 	varArray2[0] = var2[1]; // Array 2
	 	Solution [] solArrayAux = new Solution[2];
	 	
	 	solArrayAux[0] = new Solution(problem_,varArray1);
	 	solArrayAux[1] = new Solution(problem_,varArray2);
	    
	    
	 	double prob = (double) crossoverArray.getParameter("probability");
	    Solution [] offSpring = crossoverArray.doCrossover(prob, solArrayAux[0], solArrayAux[1]);

	    //-> Update the offSpring solutions
	    for (int i = 0; i < offSpring.length; i++) {
	      offSpring[i].setCrowdingDistance(0.0);
	      offSpring[i].setRank(0);
	    }
	    return offSpring;
		
	}
	
	
	
	
	public Problem get_problem() {
		return _problem;
	}
	public void set_problem(Problem _problem) {
		this._problem = _problem;
	}
}
