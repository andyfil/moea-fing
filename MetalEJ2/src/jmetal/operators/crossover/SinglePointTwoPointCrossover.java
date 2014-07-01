//  SBXSinglePointCrossover.java
//
//  Author:
//       Antonio J. Nebro <antonio@lcc.uma.es>
// 
//  Copyright (c) 2011 Antonio J. Nebro
//
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU Lesser General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU Lesser General Public License for more details.
// 
//  You should have received a copy of the GNU Lesser General Public License
//  along with this program.  If not, see <http://www.gnu.org/licenses/>.

package jmetal.operators.crossover;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import jmetal.core.Solution;
import jmetal.encodings.solutionType.ArrayIntAndPermutationSolutionType;
import jmetal.encodings.variable.Permutation;
import jmetal.util.Configuration;
import jmetal.util.JMException;
import jmetal.util.PseudoRandom;
import jmetal.util.wrapper.XInt;

public class SinglePointTwoPointCrossover extends Crossover {
	private Double intCrossoverProbability_ = null;
	private Double permutationCrossoverProbability_ = null;
	

	/**
	 * Valid solution types to apply this operator 
	 */
	@SuppressWarnings("rawtypes")
	private static final List VALID_TYPES = Arrays.asList(ArrayIntAndPermutationSolutionType.class) ;

	/**
	 * Constructor
	 */
	public SinglePointTwoPointCrossover(HashMap<String, Object> parameters) {
		super (parameters) ;

		if (parameters.get("intCrossoverProbability_") != null)
			intCrossoverProbability_ = (Double) parameters.get("intCrossoverProbability") ;  		
		if (parameters.get("permutationCrossoverProbability_") != null)
			permutationCrossoverProbability_ = (Double) parameters.get("permutationCrossoverProbability") ;  		
	} // Constructor


	/**
	 * Perform the crossover operation. 
	 * @param intProbability Crossover probability
	 * @param parent1 The first parent
	 * @param parent2 The second parent
	 * @return An array containing the two offsprings
	 */
	public Solution[] doCrossover(Double intProbability,
		Double permutationProbability,
		Solution parent1, 
		Solution parent2) throws JMException {

		Solution [] offSpring = new Solution[2];

		offSpring[0] = new Solution(parent1);
		offSpring[1] = new Solution(parent2);

		XInt x1 = new XInt(parent1) ;		
		XInt x2 = new XInt(parent2) ;		
		XInt offs1 = new XInt(offSpring[0]) ;
		XInt offs2 = new XInt(offSpring[1]) ;

		int numberOfVariables = x1.getNumberOfDecisionVariables();

		
		if (PseudoRandom.randDouble() <= intProbability) {
			//int array
			int crossoverPoint = PseudoRandom.randInt(0, numberOfVariables - 1);
			for (int i=crossoverPoint; i<numberOfVariables; i++){
				int valueX1 = x1.getValue(i);
				int valueX2 = x2.getValue(i);
				offs1.setValue(i, valueX2);
				offs2.setValue(i, valueX1);
			} // for
			
			//permutation
			int crosspoint1        ;
			int crosspoint2        ;
			int permutationLength  ;
			int parent1Vector[]    ;
			int parent2Vector[]    ;
			int offspring1Vector[] ;
			int offspring2Vector[] ;

			permutationLength = ((Permutation)parent1.getDecisionVariables()[1]).getLength();
			parent1Vector     = ((Permutation)parent1.getDecisionVariables()[1]).vector_ ;
			parent2Vector    = ((Permutation)parent2.getDecisionVariables()[1]).vector_ ;    
			offspring1Vector = ((Permutation)offSpring[0].getDecisionVariables()[1]).vector_ ;
			offspring2Vector = ((Permutation)offSpring[1].getDecisionVariables()[1]).vector_ ;

			// STEP 1: Get two cutting points
			crosspoint1 = PseudoRandom.randInt(0,permutationLength-1) ;
			crosspoint2 = PseudoRandom.randInt(0,permutationLength-1) ;

			while (crosspoint2 == crosspoint1)  
				crosspoint2 = PseudoRandom.randInt(0,permutationLength-1) ;

			if (crosspoint1 > crosspoint2) {
				int swap ;
				swap        = crosspoint1 ;
				crosspoint1 = crosspoint2 ;
				crosspoint2 = swap          ;
			} // if

			// STEP 2: Obtain the first child
			int m = 0;
			for(int j = 0; j < permutationLength; j++) {
				boolean exist = false;
				int temp = parent2Vector[j];
				for(int k = crosspoint1; k <= crosspoint2; k++) {
					if (temp == offspring1Vector[k]) {
						exist = true;
						break;
					} // if
				} // for
				if (!exist) {
					if (m == crosspoint1)
						m = crosspoint2 + 1;
					offspring1Vector[m++] = temp;
				} // if
			} // for

			// STEP 3: Obtain the second child
			m = 0;
			for(int j = 0; j < permutationLength; j++) {
				boolean exist = false;
				int temp = parent1Vector[j];
				for(int k = crosspoint1; k <= crosspoint2; k++) {
					if (temp == offspring2Vector[k]) {
						exist = true;
						break;
					} // if
				} // for
				if(!exist) {
					if (m == crosspoint1)
						m = crosspoint2 + 1;
					offspring2Vector[m++] = temp;
				} // if
			} // for

		} // if
		return offSpring;      
	} // doCrossover

	@Override
	public Object execute(Object object) throws JMException {
		Solution [] parents = (Solution [])object;
		if (parents.length != 2) {
			Configuration.logger_.severe("SBXSinglePointCrossover.execute: operator " +
			"needs two parents");
			throw new JMException("Exception in " + this.toString()+ ".execute()") ;      
		} // if

		if (!(VALID_TYPES.contains(parents[0].getType().getClass())  &&
				VALID_TYPES.contains(parents[1].getType().getClass())) ) {
			Configuration.logger_.severe("SBXSinglePointCrossover.execute: the solutions " +
					"type " + parents[0].getType() + " is not allowed with this operator");

			throw new JMException("Exception in " + this.toString()+ ".execute()") ;
		} // if 
		Solution [] offSpring;
		offSpring = doCrossover(intCrossoverProbability_, 
				permutationCrossoverProbability_, parents[0], parents[1]);

		return offSpring ;
	} // execute

} // SBXSinglePointCrossover

