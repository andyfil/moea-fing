package jmetal.encodings.solutionType;

import java.util.ArrayList;
import java.util.LinkedList;

import jmetal.core.Problem;
import jmetal.core.Solution;
import jmetal.core.SolutionType;
import jmetal.core.Variable;
import jmetal.encodings.variable.ArrayInt;
import jmetal.encodings.variable.Permutation;
import jmetal.problems.HCTScheduling;
import jmetal.util.MaquinaEstado;
import jmetal.util.TareaEstado;

public class ArrayIntAndPermutationSolutionType extends SolutionType {
	/**
	 * Constructor
	 * 
	 * @param problem
	 *            Problem being solved
	 */
	public static int cantidadMaquinas =0;
	public ArrayIntAndPermutationSolutionType(Problem problem) {
		super(problem);
		cantidadMaquinas =((HCTScheduling)problem).cantidadMaquinas;
	} // Constructor

	/**
	 * Creates the variables of the solution
	 * 
	 * @throws ClassNotFoundException
	 */
	public Variable[] createVariables() throws ClassNotFoundException {
		Variable[] variables = new Variable[2];
		int cantTareas = problem_.getLength(1);
		double [] lower = new double[cantTareas];
		double [] upper = new double[cantTareas];
		for (int i=0; i<cantTareas; i++){
			lower[i] = problem_.getLowerLimit(1);
			upper[i] = problem_.getUpperLimit(1);		}
		variables[0] = new ArrayInt(problem_.getLength(1),lower,upper);
		variables[1] = new Permutation(problem_.getLength(0));
		return variables;
	} // createVariables
	
	public static ArrayList<LinkedList<TareaEstado>> solutionToMachineList(
			Solution solution) {
		Permutation tareas;
		ArrayInt estados;
		estados = (ArrayInt) solution.getDecisionVariables()[0];
		tareas = (Permutation) solution.getDecisionVariables()[1];
		ArrayList<LinkedList<TareaEstado>> maquina_tarea_estado = new ArrayList<LinkedList<TareaEstado>>(
				cantidadMaquinas);
		for (int i = 0; i < cantidadMaquinas; i++)
			maquina_tarea_estado.add(new LinkedList<TareaEstado>());// inicializo
																	// el array
																	// list


		// First function calculo de energía
		int maqActual = 0;
		int j = 0;
		// recorro la permutación de tareas, y obtengo de la misma las tareas
		// que se ejecutan en cada maquina y en que estado
		try{
		for (int i = 0; i < tareas.getLength(); i++) {
			if (tareas.vector_[i] >= estados.getLength()) {
				maqActual = tareas.vector_[i] - estados.getLength() + 1;
			} else {
				maquina_tarea_estado.get(maqActual)
						.add(new TareaEstado(tareas.vector_[i], estados
								.getValue(j)));
				j++;
			}
		}
		}catch (Exception e){
			e.printStackTrace();
		}
		return maquina_tarea_estado;
	}
	
	public static MaquinaEstado[] solutionToTaskList(
			Solution solution) {
		Permutation tareas;
		ArrayInt estados;
		estados = (ArrayInt) solution.getDecisionVariables()[0];
		tareas = (Permutation) solution.getDecisionVariables()[1];
		int cantidadTareas = estados.getLength();
		MaquinaEstado [] tarea_maquina_estado = new MaquinaEstado[cantidadTareas];
		int maqActual = 0;
		int j = 0;
		// recorro la permutación de tareas, y obtengo de la misma las tareas
		// que se ejecutan en cada maquina y en que estado
		try{
		for (int i = 0; i < tareas.getLength(); i++) {
			if (tareas.vector_[i] >= cantidadTareas) {
				maqActual = tareas.vector_[i] - cantidadTareas + 1;
			} else {
				tarea_maquina_estado[tareas.vector_[i]] = new MaquinaEstado(maqActual, estados.getValue(j));
				j++;
			}
		}
		}catch (Exception e){
			e.printStackTrace();
		}
		return tarea_maquina_estado;
	}
}