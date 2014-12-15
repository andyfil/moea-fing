//  NSGAII.java
//
//  Author:
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

package jmetal.metaheuristics.nsgaII;

import java.util.ArrayList;
import java.util.LinkedList;

import jmetal.core.*;
import jmetal.encodings.variable.ArrayInt;
import jmetal.encodings.variable.Permutation;
import jmetal.problems.HCTScheduling;
import jmetal.qualityIndicator.QualityIndicator;
import jmetal.util.Distance;
import jmetal.util.JMException;
import jmetal.util.Ranking;
import jmetal.util.comparators.CrowdingComparator;

/**
 * Implementation of NSGA-II. This implementation of NSGA-II makes use of a
 * QualityIndicator object to obtained the convergence speed of the algorithm.
 * This version is used in the paper: A.J. Nebro, J.J. Durillo, C.A. Coello
 * Coello, F. Luna, E. Alba
 * "A Study of Convergence Speed in Multi-Objective Metaheuristics." To be
 * presented in: PPSN'08. Dortmund. September 2008.
 */

class Tarea {
	public int tarea;
	public int mejor_maquina = -1;
	public int mejor_estado = 0;
}

class TareasMaquina {
	public TareasMaquina() {
		tareas = new LinkedList<>();
	}

	public LinkedList<Integer> tareas;
	public long makespan_maquina = 0;
}

public class NSGAII extends Algorithm {
	HCTScheduling _hct = null;

	/**
	 * Constructor
	 * 
	 * @param problem
	 *            Problem to solve
	 */
	public NSGAII(Problem problem) {
		super(problem);
	} // NSGAII

	/**
	 * Runs the NSGA-II algorithm.
	 * 
	 * @return a <code>SolutionSet</code> that is a set of non dominated
	 *         solutions as a result of the algorithm execution
	 * @throws JMException
	 */
	public SolutionSet execute() throws JMException, ClassNotFoundException {
		int populationSize;
		int maxEvaluations;
		int evaluations;

		QualityIndicator indicators; // QualityIndicator object
		int requiredEvaluations; // Use in the example of use of the
		// indicators object (see below)

		SolutionSet population;
		SolutionSet offspringPopulation;
		SolutionSet union;

		Operator mutationOperator;
		Operator crossoverOperator;
		Operator selectionOperator;

		Distance distance = new Distance();

		// Read the parameters
		populationSize = ((Integer) getInputParameter("populationSize"))
				.intValue();
		maxEvaluations = ((Integer) getInputParameter("maxEvaluations"))
				.intValue();
		indicators = (QualityIndicator) getInputParameter("indicators");

		// Initialize the variables
		population = new SolutionSet(populationSize);
		evaluations = 0;

		requiredEvaluations = 0;

		// Read the operators
		mutationOperator = operators_.get("mutation");
		crossoverOperator = operators_.get("crossover");
		selectionOperator = operators_.get("selection");

		_hct = (HCTScheduling) problem_;
		// Create the initial solutionSet
		for (int i = 0; i < populationSize; i++) {
			Solution newSolution = new Solution(problem_);
			// obtener del problema las tareas, las máquinas, etc
			ArrayList<Tarea> listaTareas = new ArrayList<Tarea>(
					_hct.cantidadTareas); // Lista de tareas
			ArrayList<TareasMaquina> asignacion = new ArrayList<TareasMaquina>(); // Asignacion
																					// de
																					// tareas
																					// a
																					// maquinas

			for (int k = 0; k < _hct.cantidadMaquinas; k++) {
				asignacion.add(new TareasMaquina());
			}
			for (int j = 0; j < _hct.cantidadTareas; j++) {
				Tarea t = new Tarea();
				t.tarea = j;
				listaTareas.add(t);
			}
			// Inicializacion por mejor makespan por tarea
			while (!listaTareas.isEmpty()) {
				double indice = Math.random() * (listaTareas.size() - 1);
				Tarea candidate = listaTareas.remove((int) Math.ceil(indice));
				int mejor_maquina_tarea = -1;
				long mejor_makespan_tarea = Long.MAX_VALUE;
				for (int maq = 0; maq < _hct.cantidadMaquinas; maq++) {
					candidate.mejor_maquina = maq;
					long _value_makespan = CalculateMakespan(_hct, asignacion,
							candidate);
					if (_value_makespan <= mejor_makespan_tarea) {
						mejor_maquina_tarea = maq;
						mejor_makespan_tarea = _value_makespan;
					}
				}
				candidate.mejor_maquina = mejor_maquina_tarea;
				candidate.mejor_estado = 0;
				asignacion.get(candidate.mejor_maquina).tareas
						.add(candidate.tarea);
				asignacion.get(candidate.mejor_maquina).makespan_maquina += _hct.matriz_tiempo[candidate.mejor_maquina][candidate.mejor_estado][candidate.tarea];
			}

			// Seteo las variables de desicion
			ArrayInt estados;
			Permutation tareas;
			estados = (ArrayInt) newSolution.getDecisionVariables()[0];
			tareas = (Permutation) newSolution.getDecisionVariables()[1];
			for (int ct = 0; ct < _hct.cantidadTareas; ct++) {
				estados.setValue(ct, 0);// todas corren en estado 0
			}
			int[] _perm = tareas.vector_;
			int _perm_ind = 0;
			for (int maq = 0; maq < _hct.cantidadMaquinas; maq++) {
				LinkedList<Integer> tareas_m = asignacion.get(maq).tareas;
				if (maq != 0) {
					_perm[_perm_ind] = maq + _hct.cantidadTareas - 1;
					_perm_ind++;
				}
				if (tareas_m.size() > 0) {
					while (!tareas_m.isEmpty()) {
						_perm[_perm_ind] = tareas_m.removeFirst();
						_perm_ind++;
					}
				}
			}

			_hct.evaluate(newSolution);
			_hct.evaluateConstraints(newSolution);
			evaluations++;
			population.add(newSolution);
		} // for

		// Create the initial solutionSet
		/*
		 * Solution newSolution; for (int i = 0; i < populationSize; i++) {
		 * newSolution = new Solution(problem_);
		 * 
		 * problem_.evaluate(newSolution);
		 * problem_.evaluateConstraints(newSolution); evaluations++;
		 * population.add(newSolution); } //for
		 */

		// Generations
		while (evaluations < maxEvaluations) {

			// Create the offSpring solutionSet
			offspringPopulation = new SolutionSet(populationSize);
			Solution[] parents = new Solution[2];
			for (int i = 0; i < (populationSize / 2); i++) {
				if (evaluations < maxEvaluations) {
					// obtain parents
					parents[0] = (Solution) selectionOperator
							.execute(population);
					parents[1] = (Solution) selectionOperator
							.execute(population);
					Solution[] offSpring = (Solution[]) crossoverOperator
							.execute(parents);
					mutationOperator.execute(offSpring[0]);
					mutationOperator.execute(offSpring[1]);
					problem_.evaluate(offSpring[0]);
					problem_.evaluateConstraints(offSpring[0]);
					problem_.evaluate(offSpring[1]);
					problem_.evaluateConstraints(offSpring[1]);
					offspringPopulation.add(offSpring[0]);
					offspringPopulation.add(offSpring[1]);
					evaluations += 2;
				} // if
			} // for

			// Create the solutionSet union of solutionSet and offSpring
			union = ((SolutionSet) population).union(offspringPopulation);

			// Ranking the union
			Ranking ranking = new Ranking(union);

			int remain = populationSize;
			int index = 0;
			SolutionSet front = null;
			population.clear();

			// Obtain the next front
			front = ranking.getSubfront(index);

			while ((remain > 0) && (remain >= front.size())) {
				// Assign crowding distance to individuals
				distance.crowdingDistanceAssignment(front,
						problem_.getNumberOfObjectives());
				// Add the individuals of this front
				for (int k = 0; k < front.size(); k++) {
					population.add(front.get(k));
				} // for

				// Decrement remain
				remain = remain - front.size();

				// Obtain the next front
				index++;
				if (remain > 0) {
					front = ranking.getSubfront(index);
				} // if
			} // while

			// Remain is less than front(index).size, insert only the best one
			if (remain > 0) { // front contains individuals to insert
				distance.crowdingDistanceAssignment(front,
						problem_.getNumberOfObjectives());
				front.sort(new CrowdingComparator());
				for (int k = 0; k < remain; k++) {
					population.add(front.get(k));
				} // for

				remain = 0;
			} // if

			// This piece of code shows how to use the indicator object into the
			// code
			// of NSGA-II. In particular, it finds the number of evaluations
			// required
			// by the algorithm to obtain a Pareto front with a hypervolume
			// higher
			// than the hypervolume of the true Pareto front.
			if ((indicators != null) && (requiredEvaluations == 0)) {
				double HV = indicators.getHypervolume(population);
				if (HV >= (0.98 * indicators.getTrueParetoFrontHypervolume())) {
					requiredEvaluations = evaluations;
				} // if
			} // if
		} // while

		// Return as output parameter the required evaluations
		setOutputParameter("evaluations", requiredEvaluations);

		// Return the first non-dominated front
		Ranking ranking = new Ranking(population);
		ranking.getSubfront(0).printFeasibleFUN("FUN_NSGAII");

		return ranking.getSubfront(0);
	} // execute

	// calcula el makespan total de ejecutar la lista de tareas asignada por
	// maquinas del array más la
	// tarea recibida como parámetro
	public static long CalculateMakespan(HCTScheduling p_hct,
			ArrayList<TareasMaquina> p_asig, Tarea p_task) {
		long makespan = 0;
		for (int i = 0; i < p_hct.cantidadMaquinas; i++) {
			TareasMaquina tareas_m = p_asig.get(i);
			long _cand_makespan;
			if (p_task.mejor_maquina == i) {
				_cand_makespan = p_hct.matriz_tiempo[i][0][p_task.tarea]
						+ tareas_m.makespan_maquina;
			} else {
				_cand_makespan = tareas_m.makespan_maquina;
			}
			makespan = Math.max(makespan, _cand_makespan);
		}
		return makespan;
	}
} // NSGA-II
