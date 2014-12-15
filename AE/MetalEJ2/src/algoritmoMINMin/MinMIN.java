package algoritmoMINMin;

import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.LinkedList;

import jmetal.core.Solution;
import jmetal.core.SolutionSet;
import jmetal.encodings.variable.ArrayInt;
import jmetal.encodings.variable.Permutation;
import jmetal.problems.HCTScheduling;
import jmetal.util.JMException;

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

public class MinMIN {

	public static final int cant_tareas = 1000;
	public static final int cant_maquinas = 20;

	@SuppressWarnings("unused")
	public static void main(String[] args) {
		try {
			HCTScheduling _hct = new HCTScheduling(cant_tareas, cant_maquinas,
					4);
			Solution _sol = new Solution(_hct);
			// obtener del problema las tareas, las máquinas, etc
			int[] tasks_mac = new int[cant_tareas];// almacena cual es la
													// máquina con
													// mejor consumo energético
													// por
													// cada tarea
			ArrayList<Tarea> listaTareas = new ArrayList<Tarea>(cant_tareas);
			ArrayList<TareasMaquina> asignacion = new ArrayList<TareasMaquina>();
			for (int i = 0; i < cant_maquinas; i++) {// inicializo la lista de
														// asignacion
				// de tareas
				asignacion.add(new TareasMaquina());
			}
			for (int i = 0; i < cant_tareas; i++) {// inicializo la lista de
													// tareas a
													// asignar
				Tarea t = new Tarea();
				t.tarea = i;
				listaTareas.add(t);
			}
			// problema con que siempre inserta en la maquina que es mas rapida
			// en realacion a la energía que consume
			while (!listaTareas.isEmpty()) {
				Tarea candidate = null;
				double candidate_value = Double.MAX_VALUE;
				for (int i = 0; i < listaTareas.size(); i++) {
					Tarea _tarea = listaTareas.get(i);
					int mejor_maquina_tarea = -1;
					long mejor_makespan_tarea = Long.MAX_VALUE;
					for (int maq = 0; maq < cant_maquinas; maq++) {
						_tarea.mejor_maquina = maq;
						long _value_makespan = CalculateMakespan(_hct,
								asignacion, _tarea);
						if (_value_makespan <= mejor_makespan_tarea) {
							mejor_maquina_tarea = maq;
							mejor_makespan_tarea = _value_makespan;
						}
					}
					_tarea.mejor_maquina = mejor_maquina_tarea;
					_tarea.mejor_estado = 0;
					double _tarea_energy_value = _hct.matriz_tiempo[_tarea.mejor_maquina][0][_tarea.tarea]
							* _hct.matriz_energia[_tarea.mejor_maquina][0];
					if (_tarea_energy_value <= candidate_value) {
						candidate = _tarea;
						candidate_value = _tarea_energy_value;
					}
				}
				asignacion.get(candidate.mejor_maquina).tareas.add(candidate.tarea);
				asignacion.get(candidate.mejor_maquina).makespan_maquina += _hct.matriz_tiempo[candidate.mejor_maquina][0][candidate.tarea];
				listaTareas.remove(candidate);
			}

			ArrayInt estados;
			Permutation tareas;
			estados = (ArrayInt) _sol.getDecisionVariables()[0];
			tareas = (Permutation) _sol.getDecisionVariables()[1];
			for (int i = 0; i < cant_tareas; i++) {
				estados.setValue(i, 0);// todas corren en estado 0
			}
			int[] _perm = tareas.vector_;
			int _perm_ind = 0;
			for (int maq = 0; maq < cant_maquinas; maq++) {
				LinkedList<Integer> tareas_m = asignacion.get(maq).tareas;
				if (maq != 0) {
					_perm[_perm_ind] = maq + cant_tareas - 1;
					_perm_ind++;
				}
				if (tareas_m.size() > 0) {
					while (!tareas_m.isEmpty()) {
						_perm[_perm_ind] = tareas_m.removeFirst();
						_perm_ind++;
					}
				}
			}
			_hct.evaluate(_sol);
			double makespan = _sol.getObjective(0);
			double energy = _sol.getObjective(1);
			SolutionSet _set = new SolutionSet(1);
			_set.add(_sol);
			_set.printFeasibleVAR("VAR_Minmin");
			_set.printFeasibleFUN("FUN_Minmin");
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			e.printStackTrace();
		} catch (JMException e) {
			e.printStackTrace();
		}

	}

	// calcula el makespan total de ejecutar la lista de tareas del array más la
	// tarea recibida como parámetro
	public static long CalculateMakespan(HCTScheduling p_hct,
			ArrayList<TareasMaquina> p_asig, Tarea p_task) {
		long makespan = 0;
		for (int i = 0; i < cant_maquinas; i++) {
			TareasMaquina tareas_m = p_asig.get(i);
			long _cand_makespan;
			if( p_task.mejor_maquina == i){
				_cand_makespan = p_hct.matriz_tiempo[i][0][p_task.tarea] + tareas_m.makespan_maquina;
			}else{
				_cand_makespan = tareas_m.makespan_maquina;
			}
			makespan = Math.max(makespan, _cand_makespan);
		}
		return makespan;
	}

	// Dado un problema y una tarea devuelve la máquina que representa un menor
	// gasto energético
	public static int EvaluateEnergy(HCTScheduling p_hct, int p_tarea) {
		int candidate = -1;
		double candidate_value = Double.MAX_VALUE;
		for (int maq = 0; maq < cant_maquinas; maq++) {
			double maq_value = p_hct.matriz_tiempo[maq][0][p_tarea]
					* p_hct.matriz_energia[maq][0];
			if (maq_value <= candidate_value) {
				candidate = maq;
				candidate_value = maq_value;
			}
		}
		return candidate;
	}
}
