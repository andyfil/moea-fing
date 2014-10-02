package jmetal.operators.crossover;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Random;

import jmetal.core.Operator;
import jmetal.core.Solution;
import jmetal.encodings.solutionType.ArrayIntAndPermutationSolutionType;
import jmetal.encodings.variable.Permutation;
import jmetal.problems.HCTScheduling;
import jmetal.util.Configuration;
import jmetal.util.JMException;
import jmetal.util.MaquinaEstado;
import jmetal.util.PseudoRandom;
import jmetal.util.TareaEstado;
import jmetal.util.wrapper.XInt;

public class HCTCrossover extends Crossover {

	@SuppressWarnings("rawtypes")
	private static final List VALID_TYPES = Arrays.asList(ArrayIntAndPermutationSolutionType.class) ;
	private Double crossoverProbability_ = null;
	
	public HCTCrossover(HashMap<String, Object> parameters) {
		super(parameters);
		if (parameters.get("crossoverProbability") != null)
			crossoverProbability_ = (Double) parameters.get("crossoverProbability") ;
	}
	
	public Solution[] doCrossover(Double intProbability,
			Solution parent1, 
			Solution parent2) throws JMException {
		
		Solution [] offSpring = new Solution[2];
		
		int cantMaquinas = ((HCTScheduling)parent1.getProblem()).cantidadMaquinas;
		int cantTareas = ((HCTScheduling)parent1.getProblem()).cantidadTareas;
		//Array de largo cant de maquinas con una lista de tareas en cada maquina TareaEstado
		ArrayList<LinkedList<TareaEstado>> hijo1 = new ArrayList<LinkedList<TareaEstado>>(cantMaquinas);
		ArrayList<LinkedList<TareaEstado>> hijo2 = new ArrayList<LinkedList<TareaEstado>>(cantMaquinas);
		for(int i = 0;i<cantMaquinas;i++){
			hijo1.add(0, new LinkedList<TareaEstado>());
			hijo2.add(0,new LinkedList<TareaEstado>());
		}
		offSpring[0] = new Solution(parent1);
		offSpring[1] = new Solution(parent2);
		
		if (PseudoRandom.randDouble() <= intProbability) {
			//Array de tareas con la maquina y el estado asignados 
			MaquinaEstado [] padre1 = ArrayIntAndPermutationSolutionType.solutionToTaskList(parent1);
			MaquinaEstado [] padre2 = ArrayIntAndPermutationSolutionType.solutionToTaskList(parent2);
			for(int task=0;task<cantTareas;task++){
				double rnd = PseudoRandom.randDouble();
				MaquinaEstado me1 = padre1[task];
				MaquinaEstado me2 = padre2[task];
				LinkedList<TareaEstado> l_te1;
				LinkedList<TareaEstado> l_te2;
				TareaEstado t1;
				TareaEstado t2;
				if(rnd < 0.5){
					 l_te1= hijo1.get(me1.maquina);
					 l_te2= hijo2.get(me2.maquina);
					 t1 = new TareaEstado(task,me1.estado);
					 t2 = new TareaEstado(task,me2.estado);
				}else{
					l_te1= hijo1.get(me2.maquina);
					l_te2= hijo2.get(me1.maquina);
					t1 = new TareaEstado(task,me2.estado);
					t2 = new TareaEstado(task,me1.estado);
				}
				l_te1.add(t1);
				l_te2.add(t2);
			}
			listToSolution(offSpring[0], hijo1,cantTareas);
			listToSolution(offSpring[1], hijo2,cantTareas);
		} // if
		return offSpring;      

	}

	@Override
	public Object execute(Object object) throws JMException {
		Solution [] parents = (Solution [])object;
		if (parents.length != 2) {
			Configuration.logger_.severe("SinglePointTwoPointCrossover.execute: operator " +
			"needs two parents");
			throw new JMException("Exception in " + this.toString()+ ".execute()") ;      
		} // if

		if (!(VALID_TYPES.contains(parents[0].getType().getClass())  &&
				VALID_TYPES.contains(parents[1].getType().getClass())) ) {
			Configuration.logger_.severe("SinglePointTwoPointCrossover.execute: the solutions " +
					"type " + parents[0].getType() + " is not allowed with this operator");

			throw new JMException("Exception in " + this.toString()+ ".execute()") ;
		} // if 
		Solution [] offSpring;
		offSpring = doCrossover(crossoverProbability_,parents[0], parents[1]);

		return offSpring ;
	}

	void listToSolution(Solution offspring,ArrayList<LinkedList<TareaEstado>> hijo, int cant_tareas) throws JMException{	
		XInt off_arrayint = new XInt(offspring);
		int [] off_perm   = ((Permutation)offspring.getDecisionVariables()[1]).vector_ ;
		int perm_index = 0;
		for (int maq=0;maq<hijo.size();maq++) {
			if(maq!=0) {
				off_perm[perm_index] = cant_tareas + maq -1;
				perm_index++;
			}
			if(hijo.get(maq)!= null)
				for(TareaEstado t : hijo.get(maq)){
					off_arrayint.setValue(t.tarea, t.estado);
					off_perm[perm_index] = t.tarea;
					perm_index ++;
				}
			}
		}
}
