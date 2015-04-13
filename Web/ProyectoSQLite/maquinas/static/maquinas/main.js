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