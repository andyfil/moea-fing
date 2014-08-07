//  pNSGAII_Settings.java 
//
//  Authors:
//       Antonio J. Nebro <antonio@lcc.uma.es>
//
//  Copyright (c) 2013 Antonio J. Nebro
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

package jmetal.experiments.settings;

import jmetal.core.Algorithm;
import jmetal.experiments.Settings;
import jmetal.metaheuristics.nsgaII.pNSGAII;
import jmetal.operators.crossover.Crossover;
import jmetal.operators.crossover.CrossoverFactory;
import jmetal.operators.mutation.Mutation;
import jmetal.operators.mutation.MutationFactory;
import jmetal.operators.selection.Selection;
import jmetal.operators.selection.SelectionFactory;
import jmetal.problems.HCTScheduling;
import jmetal.util.JMException;
import jmetal.util.parallel.IParallelEvaluator;
import jmetal.util.parallel.MultithreadedEvaluator;

import java.io.FileNotFoundException;
import java.util.HashMap;
import java.util.Properties;

/**
 * Settings class of algorithm pNSGA-II (real encoding)
 */
public class pNSGAII_Settings extends Settings {
	  public int populationSize_                 ;
	  public int maxEvaluations_                 ;
	  public double mutationProbability_         ;
	  public double crossoverProbability_        ;
	  public int    numberOfThreads_             ;
  
  /**
   * Constructor
   */
  public pNSGAII_Settings(String problem) {
    super(problem) ;
    

    try {
		problem_ = new HCTScheduling(100,20,4);
	} catch (FileNotFoundException e) {
		e.printStackTrace();
	}  
    // Default experiments.settings
    populationSize_              = 50   ; 
    maxEvaluations_              = 25000 ;
    mutationProbability_         = 0.1 ;
    crossoverProbability_        = 0.5   ;
    numberOfThreads_             = 4 ; // 0 - number of available cores
  } // pNSGAII_Settings

  
  /**
   * Configure NSGAII with user-defined parameter experiments.settings
   * @return A NSGAII algorithm object
   * @throws jmetal.util.JMException
   */
  @SuppressWarnings({ "unchecked", "rawtypes" })
public Algorithm configure() throws JMException {
    Algorithm algorithm ;
    Selection  selection ;
    Crossover  crossover ;
    Mutation   mutation  ;

    HashMap  parameters ; // Operator parameters

    IParallelEvaluator parallelEvaluator = new MultithreadedEvaluator(numberOfThreads_) ;

    // Creating the algorithm. 
    algorithm = new pNSGAII(problem_, parallelEvaluator) ;
    
    // Algorithm parameters
    algorithm.setInputParameter("populationSize",populationSize_);
    algorithm.setInputParameter("maxEvaluations",maxEvaluations_);

    // Mutation and Crossover for Real codification
    parameters = new HashMap() ;
    parameters.put("probability", crossoverProbability_) ;
    crossover = CrossoverFactory.getCrossoverOperator("SinglePointTwoPointCrossover", parameters);                   

    parameters = new HashMap() ;
    parameters.put("intMutationProbability", mutationProbability_);
    parameters.put("permutationMutationProbability", mutationProbability_);
    mutation = MutationFactory.getMutationOperator("BitFlipSwapMutation", parameters);                        

    // Selection Operator 
    parameters = null ;
    selection = SelectionFactory.getSelectionOperator("BinaryTournament2", parameters) ;     

    // Add the operators to the algorithm
    algorithm.addOperator("crossover",crossover);
    algorithm.addOperator("mutation",mutation);
    algorithm.addOperator("selection",selection);
    
    return algorithm ;
  } // configure

  /**
   * Configure pNSGAII with user-defined parameter experiments.settings
   * @return A pNSGAII algorithm object
   */
  @SuppressWarnings({ "unchecked", "rawtypes" })
@Override
  public Algorithm configure(Properties configuration) throws JMException {
    Algorithm algorithm ;
    Selection  selection ;
    Crossover  crossover ;
    Mutation   mutation  ;

    HashMap  parameters ; // Operator parameters

    numberOfThreads_ = Integer.parseInt(configuration.getProperty("numberOfThreads",String.valueOf(numberOfThreads_)));

    IParallelEvaluator parallelEvaluator = new MultithreadedEvaluator(numberOfThreads_) ;

    // Creating the algorithm.
    algorithm = new pNSGAII(problem_, parallelEvaluator) ;

    // Algorithm parameters
    populationSize_ = Integer.parseInt(configuration.getProperty("populationSize",String.valueOf(populationSize_)));
    maxEvaluations_  = Integer.parseInt(configuration.getProperty("maxEvaluations",String.valueOf(maxEvaluations_)));
    algorithm.setInputParameter("populationSize",populationSize_);
    algorithm.setInputParameter("maxEvaluations",maxEvaluations_);

    // Mutation and Crossover for Real codification
    crossoverProbability_ = Double.parseDouble(configuration.getProperty("crossoverProbability",String.valueOf(crossoverProbability_)));
    parameters = new HashMap() ;
    parameters.put("probability", crossoverProbability_) ;
    crossover = CrossoverFactory.getCrossoverOperator("SinglePointTwoPointCrossover", parameters);

    mutationProbability_ = Double.parseDouble(configuration.getProperty("mutationProbability",String.valueOf(mutationProbability_)));
    parameters = new HashMap() ;
    parameters.put("probability", mutationProbability_) ;
    mutation = MutationFactory.getMutationOperator("BitFlipSwapMutation", parameters);

    // Selection Operator
    parameters = null ;
    selection = SelectionFactory.getSelectionOperator("BinaryTournament2", parameters) ;

    // Add the operators to the algorithm
    algorithm.addOperator("crossover",crossover);
    algorithm.addOperator("mutation",mutation);
    algorithm.addOperator("selection",selection);

    return algorithm ;
  }
} //pNSGAII_Settings
