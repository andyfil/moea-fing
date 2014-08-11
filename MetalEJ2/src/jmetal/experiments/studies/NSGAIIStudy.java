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

			parameters[0].put("crossoverProbability_", 0.8);
			parameters[1].put("crossoverProbability_", 0.6);
			parameters[2].put("crossoverProbability_", 0.4);
			parameters[3].put("mutationProbability_", 0.1);
			parameters[4].put("mutationProbability_", 0.05);
			parameters[5].put("mutationProbability_", 0.01);
			parameters[6].put("populationSize_", 50);
			parameters[7].put("populationSize_", 100);
			parameters[8].put("populationSize_", 200);

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
		exp.algorithmNameList_ = new String[] { "NSGAIIa", "NSGAIIb",
				"NSGAIIc", "NSGAIId","NSGAIIe","NSGAIIf","NSGAIIg","NSGAIIh","NSGAIIi" };
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

