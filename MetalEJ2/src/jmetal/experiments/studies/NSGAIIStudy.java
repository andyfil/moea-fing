//  NSGAIIStudy.java
//
//  Authors:
//       Antonio J. Nebro <antonio@lcc.uma.es>
//       Juan J. Durillo <durillo@lcc.uma.es>
//
//  Copyright (c) 2011 Antonio J. Nebro, Juan J. Durillo
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

package jmetal.experiments.studies;

import jmetal.core.Algorithm;
import jmetal.experiments.Experiment;
import jmetal.experiments.Settings;
import jmetal.experiments.settings.NSGAII_Settings;
import jmetal.experiments.util.Friedman;
import jmetal.util.JMException;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.HashMap;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Class implementing an example of experiment using NSGA-II as base algorithm.
 * The experiment consisting in studying the effect of the crossover probability
 * in NSGA-II.
 */
public class NSGAIIStudy extends Experiment {
	/**
	 * Configures the algorithms in each independent run
	 * 
	 * @param problemName
	 *            The problem to solve
	 * @param problemIndex
	 * @param algorithm
	 *            Array containing the algorithms to run
	 * @throws ClassNotFoundException
	 * @throws FileNotFoundException
	 */
	@SuppressWarnings({ "unchecked", "rawtypes" })
	public synchronized void algorithmSettings(String problemName,
			int problemIndex, Algorithm[] algorithm)
			throws ClassNotFoundException, FileNotFoundException {
		try {
			int numberOfAlgorithms = algorithmNameList_.length;

			HashMap[] parameters = new HashMap[numberOfAlgorithms];

			for (int i = 0; i < numberOfAlgorithms; i++) {
				parameters[i] = new HashMap();
			} // for

			// NSGAII0: crossoverProbability-> 0.4 |  mutationProbability-> 0.01 | populationSize-> 50
			parameters[0].put("crossoverProbability_", 0.4);
			parameters[0].put("mutationProbability_", 0.01);
			parameters[0].put("populationSize_", 50);
			// NSGAII1: crossoverProbability-> 0.4 |  mutationProbability-> 0.01 | populationSize-> 100
			parameters[1].put("crossoverProbability_", 0.4);
			parameters[1].put("mutationProbability_", 0.01);
			parameters[1].put("populationSize_", 100);
			// NSGAII2: crossoverProbability-> 0.4 |  mutationProbability-> 0.01 | populationSize-> 200
			parameters[2].put("crossoverProbability_", 0.4);
			parameters[2].put("mutationProbability_", 0.01);
			parameters[2].put("populationSize_", 200);
			// NSGAII3: crossoverProbability-> 0.4 |  mutationProbability-> 0.05 | populationSize-> 50
			parameters[3].put("crossoverProbability_", 0.4);
			parameters[3].put("mutationProbability_", 0.05);
			parameters[3].put("populationSize_", 50);
			// NSGAII4: crossoverProbability-> 0.4 |  mutationProbability-> 0.05 | populationSize-> 100
			parameters[4].put("crossoverProbability_", 0.4);
			parameters[4].put("mutationProbability_", 0.05);
			parameters[4].put("populationSize_", 100);
			// NSGAII5: crossoverProbability-> 0.4 |  mutationProbability-> 0.05 | populationSize-> 200
			parameters[5].put("crossoverProbability_", 0.4);
			parameters[5].put("mutationProbability_", 0.05);
			parameters[5].put("populationSize_", 200);
			// NSGAII6: crossoverProbability-> 0.4 |  mutationProbability-> 0.1  | populationSize-> 50
			parameters[6].put("crossoverProbability_", 0.4);
			parameters[6].put("mutationProbability_", 0.1);
			parameters[6].put("populationSize_", 50);
			// NSGAII7: crossoverProbability-> 0.4 |  mutationProbability-> 0.1  | populationSize-> 100
			parameters[7].put("crossoverProbability_", 0.4);
			parameters[7].put("mutationProbability_", 0.1);
			parameters[7].put("populationSize_", 100);
			// NSGAII8: crossoverProbability-> 0.4 |  mutationProbability-> 0.1  | populationSize-> 200
			parameters[8].put("crossoverProbability_", 0.4);
			parameters[8].put("mutationProbability_", 0.1);
			parameters[8].put("populationSize_", 200);
			// NSGAII9: crossoverProbability-> 0.6 |  mutationProbability-> 0.01 | populationSize-> 50
			parameters[9].put("crossoverProbability_", 0.6);
			parameters[9].put("mutationProbability_", 0.01);
			parameters[9].put("populationSize_", 50);
			// NSGAII10: crossoverProbability-> 0.6 |  mutationProbability-> 0.01 | populationSize-> 100
			parameters[10].put("crossoverProbability_", 0.6);
			parameters[10].put("mutationProbability_", 0.01);
			parameters[10].put("populationSize_", 100);
			// NSGAII11: crossoverProbability-> 0.6 |  mutationProbability-> 0.01 | populationSize-> 200
			parameters[11].put("crossoverProbability_", 0.6);
			parameters[11].put("mutationProbability_", 0.01);
			parameters[11].put("populationSize_", 200);
			// NSGAII12: crossoverProbability-> 0.6 |  mutationProbability-> 0.05 | populationSize-> 50
			parameters[12].put("crossoverProbability_", 0.6);
			parameters[12].put("mutationProbability_", 0.05);
			parameters[12].put("populationSize_", 50);
			// NSGAII13: crossoverProbability-> 0.6 |  mutationProbability-> 0.05 | populationSize-> 100
			parameters[13].put("crossoverProbability_", 0.6);
			parameters[13].put("mutationProbability_", 0.05);
			parameters[13].put("populationSize_", 100);
			// NSGAII14: crossoverProbability-> 0.6 |  mutationProbability-> 0.05 | populationSize-> 200
			parameters[14].put("crossoverProbability_", 0.6);
			parameters[14].put("mutationProbability_", 0.05);
			parameters[14].put("populationSize_", 200);
			// NSGAII15: crossoverProbability-> 0.6 |  mutationProbability-> 0.1  | populationSize-> 50
			parameters[15].put("crossoverProbability_", 0.6);
			parameters[15].put("mutationProbability_", 0.1);
			parameters[15].put("populationSize_", 50);
			// NSGAII16: crossoverProbability-> 0.6 |  mutationProbability-> 0.1  | populationSize-> 100
			parameters[16].put("crossoverProbability_", 0.6);
			parameters[16].put("mutationProbability_", 0.1);
			parameters[16].put("populationSize_", 100);
			// NSGAII17: crossoverProbability-> 0.6 |  mutationProbability-> 0.1  | populationSize-> 200
			parameters[17].put("crossoverProbability_", 0.6);
			parameters[17].put("mutationProbability_", 0.1);
			parameters[17].put("populationSize_", 200);
			// NSGAII18: crossoverProbability-> 0.8 |  mutationProbability-> 0.01 | populationSize-> 50
			parameters[18].put("crossoverProbability_", 0.8);
			parameters[18].put("mutationProbability_", 0.01);
			parameters[18].put("populationSize_", 50);
			// NSGAII19: crossoverProbability-> 0.8 |  mutationProbability-> 0.01 | populationSize-> 100
			parameters[19].put("crossoverProbability_", 0.8);
			parameters[19].put("mutationProbability_", 0.01);
			parameters[19].put("populationSize_", 100);
			// NSGAII20: crossoverProbability-> 0.8 |  mutationProbability-> 0.01 | populationSize-> 200
			parameters[20].put("crossoverProbability_", 0.8);
			parameters[20].put("mutationProbability_", 0.01);
			parameters[20].put("populationSize_", 200);
			// NSGAII21: crossoverProbability-> 0.8 |  mutationProbability-> 0.05 | populationSize-> 50
			parameters[21].put("crossoverProbability_", 0.8);
			parameters[21].put("mutationProbability_", 0.05);
			parameters[21].put("populationSize_", 50);
			// NSGAII22: crossoverProbability-> 0.8 |  mutationProbability-> 0.05 | populationSize-> 100
			parameters[22].put("crossoverProbability_", 0.8);
			parameters[22].put("mutationProbability_", 0.05);
			parameters[22].put("populationSize_", 100);
			// NSGAII23: crossoverProbability-> 0.8 |  mutationProbability-> 0.05 | populationSize-> 200
			parameters[23].put("crossoverProbability_", 0.8);
			parameters[23].put("mutationProbability_", 0.05);
			parameters[23].put("populationSize_", 200);
			// NSGAII24: crossoverProbability-> 0.8 |  mutationProbability-> 0.1  | populationSize-> 50
			parameters[24].put("crossoverProbability_", 0.8);
			parameters[24].put("mutationProbability_", 0.1);
			parameters[24].put("populationSize_", 50);
			// NSGAII25: crossoverProbability-> 0.8 |  mutationProbability-> 0.1  | populationSize-> 100
			parameters[25].put("crossoverProbability_", 0.8);
			parameters[25].put("mutationProbability_", 0.1);
			parameters[25].put("populationSize_", 100);
			// NSGAII26: crossoverProbability-> 0.8 |  mutationProbability-> 0.1  | populationSize-> 200
			parameters[26].put("crossoverProbability_", 0.8);
			parameters[26].put("mutationProbability_", 0.1);
			parameters[26].put("populationSize_", 200);
			
			for (int i = 0; i < numberOfAlgorithms; i++)
				algorithm[i] = new NSGAII_Settings(problemName)
						.configure(parameters[i]);

		} catch (IllegalArgumentException ex) {
			Logger.getLogger(NSGAIIStudy.class.getName()).log(Level.SEVERE,
					null, ex);
		} catch (IllegalAccessException ex) {
			Logger.getLogger(NSGAIIStudy.class.getName()).log(Level.SEVERE,
					null, ex);
		} catch (JMException ex) {
			Logger.getLogger(NSGAIIStudy.class.getName()).log(Level.SEVERE,
					null, ex);
		}
	} // algorithmSettings

	public static void main(String[] args) throws JMException, IOException {
		NSGAIIStudy exp = new NSGAIIStudy(); // exp = experiment

		exp.experimentName_ = "HTCEstudio";
		exp.algorithmNameList_ = new String[] { "NSGAII0", "NSGAII1",
				"NSGAII2", "NSGAII3","NSGAII4","NSGAII5","NSGAII6","NSGAII7","NSGAII8", "NSGAII9", "NSGAII10",
				"NSGAII11", "NSGAII12","NSGAII13","NSGAII14","NSGAII15","NSGAII16","NSGAII17", "NSGAII18", "NSGAII19",
				"NSGAII20", "NSGAII21","NSGAII22","NSGAII23","NSGAII24","NSGAII25","NSGAII26" };
		exp.problemList_ = new String[] { "HCTScheduling" };
		exp.paretoFrontFile_ = new String [1];
		exp.indicatorList_ = new String[] { "HV", "SPREAD", "IGD", "EPSILON" };

		int numberOfAlgorithms = exp.algorithmNameList_.length;

		exp.experimentBaseDirectory_ = "C:\\"
				+ exp.experimentName_;
		exp.paretoFrontDirectory_ = "";

		exp.algorithmSettings_ = new Settings[numberOfAlgorithms];

		exp.independentRuns_ = 5;

		exp.initExperiment();

		// Run the experiments
		exp.runExperiment(4);

		exp.generateQualityIndicators();

		// Generate latex tables (comment this sentence is not desired)
		exp.generateLatexTables();

		// Configure the R scripts to be generated
		int rows;
		int columns;
		String prefix;
		String[] problems;

		rows = 2;
		columns = 3;
		prefix = new String("Problems");
		problems = new String[] { "HCTScheduling" };

		boolean notch;
		exp.generateRBoxplotScripts(rows, columns, problems, prefix,
				notch = true, exp);
		exp.generateRWilcoxonScripts(problems, prefix, exp);

		// Applying Friedman test
		Friedman test = new Friedman(exp);
		test.executeTest("EPSILON");
		test.executeTest("HV");
		test.executeTest("SPREAD");
	} // main
} // NSGAIIStudy

