function makegraphic(){
	
	var data, g

	data = "Date,Temperature\n"
	data += "2008-05-07,75\n"
	data += "2008-05-08,70\n" +
	data += "2008-05-09,80\n"		
	
	g = new Dygraph(document.getElementById("graphdiv"), data, {
																  legend: 'always',
																  title: 'NYC vs. SF',
																  showRoller: true,
																  rollPeriod: 14,
																  customBars: true,
																  ylabel: 'Temperature (F)',
																}
					);

}

function relojFecha(){
 	var mydate=new Date();var year=mydate.getYear();
 	if (year < 1000)year+=1900;
 	var day=mydate.getDay();
 	var month=mydate.getMonth();
 	var daym=mydate.getDate();
 	if (daym<10)daym="0"+daym;
 	var dayarray=new Array("Domingo","Lunes","Martes","Miercoles","Jueves","Viernes","Sabado");
 	var montharray=new Array("Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto",
 	                                             "Septiembre","Octubre","Noviembre","Diciembre");
 	var horas = mydate.getHours();
 	horas = (horas<10)?"0"+horas:horas;
 	var minutos = mydate.getMinutes();
 	minutos = (minutos<10)?"0"+minutos:minutos;
 	var segundos = mydate.getSeconds();
 	segundos = (segundos<10)?"0"+segundos:segundos;
 	document.getElementById("idReloj").innerHTML = "<"+"small><"+"font color='000000' face='Verdana'>"+
 	                                                dayarray[day]+" "+daym+" de "+montharray[month]+" de "+
                                                        year+" "+horas+":"+minutos+":"+segundos+"<"+"/font><"+"/small>";
 	setTimeout('relojFecha()',1000);
}