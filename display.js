$(function() {
    var cue = "circle[fill='WHITE']";
    var line = "line"
    var line2 = "#myCanvas";
    $(line2).attr("visibility", "hidden");
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
  
  
    });
    $(document).mouseup(function(e) {
      
      $(cue).attr("r", "28");
      $(line).attr("visibility", "hidden");
      $(line2).attr("visibility", "hidden");
      var xDiff = $(line).attr("x2") - $(line).attr("x1");
      var yDiff = $(line).attr("y2") - $(line).attr("y1");
      xDiff = xDiff * 5;
      yDiff = yDiff * 5;
      setLine();
      $(document).unbind('mousemove');
      if (xDiff != 0 || yDiff != 0) {
        $.post("post.html",{
          xVel: xDiff,
          yVel: yDiff
        },
        function(rep){
          var str = JSON.stringify(rep);
          var arr = str.split(",");
          setInterval("anim()", 10);
          var i = 0;
          function anim(){
            $(document).replaceWith(arr[i]);
            if (arr.length == i){
              return;
            }
          }
        }
        )
        .fail(function(){
          alert("oops");
        })
        
      }
      
    });
  
    function setLine() { // put it with cue ball
      var coord = svgToCanvas($(cue).attr("cx"), $(cue).attr("cy")); // convert cue to real coordinates
      var coord2 = svgPoint(coord.x, coord.y, "line"); // convert to svg coords in line svg
      $(line).attr("x1", coord2.x);
      $(line).attr("y1", coord2.y);
      $(line).attr("x2", coord2.x);
      $(line).attr("y2", coord2.y);
    }
  })
  