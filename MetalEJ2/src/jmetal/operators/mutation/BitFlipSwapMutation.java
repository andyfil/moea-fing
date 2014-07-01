//  PolynomialBitFlipMutation.java
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

package jmetal.operators.mutation;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import jmetal.core.Solution;
import jmetal.encodings.solutionType.ArrayRealAndBinarySolutionType;
import jmetal.encodings.variable.Permutation;
import jmetal.util.Configuration;
import jmetal.util.JMException;
import jmetal.util.PseudoRandom;
import jmetal.util.wrapper.XInt;

public class BitFlipSwapMutation extends Mutation {
	private Double intMutationProbability_ = null;
	private Double permutationMutationProbability_ = null;

	/**
	 * Valid solution types to apply this operator
	 */
	@SuppressWarnings("rawtypes")
	private static final List VALID_TYPES = Arrays
			.asList(ArrayRealAndBinarySolutionType.class);

	/**
	 * Constructor
	 */
	public BitFlipSwapMutation(HashMap<String, Object> parameters) {
		super(parameters);
		if (parameters.get("realMutationProbability") != null)
			intMutationProbability_ = (Double) parameters
					.get("intMutationProbability");
		if (parameters.get("binaryMutationProbability") != null)
			permutationMutationProbability_ = (Double) parameters
					.get("permutationMutationProbability");
	}

	@Override
	public Object execute(Object object) throws JMException {
		Solution solution = (Solution) object;

		if (!VALID_TYPES.contains(solution.getType().getClass())) {
			Configuration.logger_
					.severe("PolynomialBitFlipMutation.execute: the solution "
							+ "type " + solution.getType()
							+ " is not allowed with this operator");

			throw new JMException("Exception in " + this.toString()
					+ ".execute()");
		} // if

		doMutation(intMutationProbability_, permutationMutationProbability_,
				solution);
		return solution;
	} // execute

	/**
	 * doMutation method
	 * 
	 * @param intProbability
	 * @param permutationProbability
	 * @param solution
	 * @throws JMException
	 */
	public void doMutation(Double intProbability,
			Double permutationProbability, Solution solution)
			throws JMException {
		XInt x = new XInt(solution);
		// Integer representation
		for (int i = 0; i < x.getNumberOfDecisionVariables(); i++)
			if (PseudoRandom.randDouble() < intProbability) {
				int value = PseudoRandom.randInt(x.getLowerBound(i),x.getUpperBound(i));
				x.setValue(i, value);
			} // if

	      int permutationLength = ((Permutation)solution.getDecisionVariables()[1]).getLength() ;
	      int [] permutation = ((Permutation)solution.getDecisionVariables()[1]).vector_ ;

	      if (PseudoRandom.randDouble() < permutationProbability) {
	        int pos1 ;
	        int pos2 ;

	        pos1 = PseudoRandom.randInt(0,permutationLength-1) ;
	        pos2 = PseudoRandom.randInt(0,permutationLength-1) ;

	        while (pos1 == pos2) {
	          if (pos1 == (permutationLength - 1)) 
	            pos2 = PseudoRandom.randInt(0, permutationLength- 2);
	          else 
	            pos2 = PseudoRandom.randInt(pos1, permutationLength- 1);
	        } // while
	        // swap
	        int temp = permutation[pos1];
	        permutation[pos1] = permutation[pos2];
	        permutation[pos2] = temp;    
	      } // if
	} // doMutation
} // PolynomialBitFlipMutation

