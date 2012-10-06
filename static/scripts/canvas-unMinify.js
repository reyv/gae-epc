function drawWall(Beta,Alpha) {
  var canvas = document.getElementById('canvas');
  var beta = Number(Beta);
  var alpha = Number(Alpha);
  var context = canvas.getContext('2d');		
  var centerX = canvas.width/2;					//Center of Canvas
  var centerY = canvas.height/2;
  canvas.width = canvas.width;					//This clears the canvas every time this function is called
  canvas.height = canvas.height;
  //<------------------ Start Draw actual wall
  var top_bottom_width = 25;					//arbitrary width to make it look nice on canvas (trial/error)
  var left_height = 130;						//arbitrary height to make it look nice on canvas(trial/error)       
  var extra_bottom_width = left_height/Math.tan(beta*Math.PI/180); //calculates additional wall width as a result of the wall inclination
   
  if(beta===90 || beta > 90){			//limit wall inclination to 90 degrees for obvious reasons
	extra_bottom_width=0;
  }else if (beta<65){					//Limit wall inclination to 65 deg.
	extra_bottom_width=60.6;
  }
  context.beginPath();
  context.moveTo(50,65);
  context.lineTo(50,65+left_height);
  context.lineTo(50+top_bottom_width,65+left_height);
  context.lineTo(50+top_bottom_width+extra_bottom_width,65+left_height);
  context.lineTo(50+top_bottom_width,65);
  context.lineTo(50,65); 
  context.lineWidth = 3;				//Set lines and draw wall. Default is black
  context.fillStyle='#00B4E5';
  context.stroke();
  context.fill();
  //<------------------ End Draw wall geometry
  //<------------------ Start Draw bottom horizontal bar (i.e. groundline)
 context.beginPath();
  if(beta===90 || beta>90){					//limit wall inclination to 90 degrees for obvious reasons
    context.moveTo(75,195);
	context.lineTo(250,195);
  }else if(beta<65){						//Limit wall inclination to 65 deg.
    context.moveTo(50+top_bottom_width+60.6,195);
	context.lineTo(250,195);
  }else{
    context.moveTo(50+top_bottom_width+extra_bottom_width,195);
	context.lineTo(250,195);
  }
  //<------------------ End Draw bottom horizontal bar (i.e. groundline)
  //<------------------- Start Draw backfill inclination
  var backfill_bottom_width = 175;				//arbitrary
  var backfill_extra_height = backfill_bottom_width*Math.tan(alpha*Math.PI/180);
   
  if(alpha>25){									//Limit drawing on canvas to alpha=25 degrees
    backfill_extra_height = 81.6;
  }else if(alpha<0){
	backfill_extra_height=0;
  }
  context.moveTo(75,65);
  context.lineTo(165,65-backfill_extra_height);
  context.moveTo(75,65);
  context.lineTo(250,65);
  context.lineWidth = 2;						//default is black
  context.stroke();
  //<------------------- End Draw backfill inclination
  //<------------------- Start Arc for wall inclination
  var betaRadius = 10;
  var arc_beta_x = 50+top_bottom_width+extra_bottom_width;
  var arc_beta_y = 195;
  var startAngle = 1*Math.PI;
  var endAngle = 1.45*Math.PI;
  var betaTextPositionX = 52+extra_bottom_width;  			// good place for Beta = 65 deg.
  var betaTextPositionY = 180;
  
  if(beta===90 || beta>90){
	endAngle = 1.5*Math.PI;
  }else if (beta<=65){
	endAngle = 1.35*Math.PI;
  }
  context.beginPath();
  context.arc(arc_beta_x,arc_beta_y, betaRadius, startAngle, endAngle, false);
  context.lineWidth = 1.5;						//default is black
  context.stroke();
  //<------------------- End Arc for wall inclination 
  //<------------------- // Start Arc for backfill inclination
  var alphaRadius = 15;
  var alphaRadians = alpha*Math.PI/180;
  var arc_alpha_x = 90;
  var arc_alpha_y = 65;
  var alphaStartAngle = 0;
  var alphaEndAngle = (2-alpha*2/100)*Math.PI;
  var alphaTextPositionX = 115;
  var alphaTextPositionY = 60;
      
  if(alpha<=0){
    alphaRadius = 0;
    arc_alpha_x = 0;
    arc_alpha_y = 0;
    alphaStartAngle = 0;
    alphaEndAngle = 0;
    alphaTextPositionX = 0;
    alphaTextPositionY = 0;
}else if (alpha>=25){
	alphaEndAngle = 4.7124;
}
  context.beginPath();
  context.arc(arc_alpha_x,arc_alpha_y, alphaRadius, alphaStartAngle, alphaEndAngle, true);
  context.lineWidth = 1.5;					//default is black
  context.stroke();
  //<------------------- End Arc for backfill inclination
  //<------------------- Start Text for canvas
  context.fillStyle='black';
  context.font="bold 10pt arial";
  context.fillText("Granular Fill",160,125);    
  context.fillText("Backfill",170,55);  
  context.fillText("β",betaTextPositionX,betaTextPositionY); 
  context.fillText("α",alphaTextPositionX,alphaTextPositionY); 
  //<------------------- End Text for canvas
}