$(function() {
	var cue = "circle[fill='WHITE']";
	var line = "line"
	var line2 = "#myCanvas";
	$(line2).attr("visibility", "hidden");
	var p1 = "#p1S";
	var p2 = "#p2S";
	var p1Balls = 0;
	var p2Balls = 0;
	var currP = Math.floor(Math.random() * 2);
	alert("player " + (currP + 1) + " is first");
	setLine();

	function svgPoint(screenX, screenY, query) {
		var p = new DOMPoint(screenX, screenY);
		var svg = document.querySelector(query);
		return p.matrixTransform(svg.getScreenCTM().inverse());
	}

	function svgToCanvas(x, y) {
		var p = new DOMPoint(x, y);
		var svg = document.querySelector("circle[fill ='WHITE']");
		return p.matrixTransform(svg.getScreenCTM());
	}

	function dist(x1, x2, y1, y2) {
		return Math.sqrt((x2 -= x1) * x2 + (y2 -= y1) * y2);
	}

	$(cue).mousedown(function() {
		cueDown($(cue));
	});
	function arraySum(inp){
		var sum = 0;
		for (var i =0; i < inp.length; i++){
			sum += Number(inp[i]);
		}
		return sum;
	}

	function cueDown() {
		$(this).attr("r", "35");
		$(document).mousemove(function(e) {

			$(line).attr("visibility", "visible");
			$(line2).attr("visibility", "visible");
			var coord = svgPoint(e.clientX, e.clientY, "line");

			var len = dist($(line).attr("x1"), coord.x,
				$(line).attr("y1"), coord.y);
			len = len * 5;
			//console.log(len);
			var color;
			if (len <= 4000) {
				$(line).attr("x2", coord.x);
				$(line).attr("y2", coord.y);
				color = "hsl(" + (180 - ((len / 4000) * 180)) + ", 100%, 60%)";
				$(line).attr("stroke-width", (len / 4000) * 25);
				$(line).attr("stroke", color);
			}
		});
	}
	$(document).mouseup(function(e) {

		$(cue).attr("r", "28");
		$(line).attr("visibility", "hidden");
		$(line2).attr("visibility", "hidden");
		var xDiff = $(line).attr("x2") - $(line).attr("x1");
		var yDiff = $(line).attr("y2") - $(line).attr("y1");
		xDiff = xDiff * 5;
		yDiff = yDiff * 5;

		if (xDiff != 0 || yDiff != 0) {
			$.post("post", { // POST REQUEST.
						xVel: xDiff * -1,
						yVel: yDiff * -1
					},
					function(rep) {

						var arr = rep.split(",");
						var ballArr = arr[arr.length - 1].split("#");
						var p1Arr = ballArr.slice(1,8);
						var p2Arr = ballArr.slice(9,16);
						//alert(ballArr);
						setInterval(anim, 10);
						var i = 0;
						
						function anim() {
							i++;

							if (arr.length - 1 == (i)) {
								if (ballArr[8] == 0 ){
									if (currP == 0){
										if (arraySum(p1Arr) > 0){
											alert("P!AYER 1 LOST BY ILLEGALLY POTTING THE 8 BALL");
										}
										else{
											alert("player 1 wins");
										}
									}
									else if (currP == 1){
										if (arraySum(p2Arr) > 0){
											alert("PLAYER 2 LOST BY ILLEGALLY POTTING THE 8 BALL");
										}
										else{
											alert("player 2 wins");
										}
									}
								}
								else{
									if (ballArr[0] == 0) {

										respawnCue();
									} else {

										clearInterval();
										refreshCue();
									}

									p1Balls =arraySum(p1Arr);
									p2Balls = arraySum(p2Arr);

									$(p1).html(p1Balls +" ball(s) left");
									$(p2).html(p2Balls +" ball(s) left");
									currP = !currP;
									alert("current player is " + (currP+1));
								}
							} else {
								$("div#inner").html(arr[i]);
							}
							
						}

					}
				)
				.fail(function() {
					alert("oops");
				})

		}
		setLine();
		$(document).unbind('mousemove');
	});

	function refreshCue() {
		setLine();
		$(document).unbind('mousemove');
		$(cue).mousedown(function() {
			cueDown($(cue));
		});
	}
	function respawnCue(){
		$.post("respawn", { }, 
		function(rep){
			$('#table').fadeOut("slow", function(){
				
				$(this).replaceWith(rep);
				$('#table').fadeIn("slow");
				refreshCue();
			});
		})
		.fail(function(){
			alert("respawn failed");
		})
	}



	function setLine() { // put it with cue ball
		var coord = svgToCanvas($(cue).attr("cx"), $(cue).attr("cy")); // convert cue to real coordinates
		var coord2 = svgPoint(coord.x, coord.y, "line"); // convert to svg coords in line svg
		$(line).attr("x1", coord2.x);
		$(line).attr("y1", coord2.y);
		$(line).attr("x2", coord2.x);
		$(line).attr("y2", coord2.y);
	}
})