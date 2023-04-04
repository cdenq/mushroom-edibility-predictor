document.querySelector("#predictButton").addEventListener("click", function(event) {
  event.preventDefault();
  prediction()
});

async function prediction(){
  //display spinner
  document.getElementById('spinner').style.display = 'block';
  
  //build object to pass
  let feature_list = {};
  //all user input elements
  let selections = document.getElementsByClassName('mushroom_traits');
  for (let i = 0; i < selections.length; i++) {
      feature_list[selections[i].id] = selections[i].value;
  };

  //call flask route
  let response = await fetch('/predict', {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(feature_list), 
      cache: "no-cache",
      headers: new Headers({
          "content-type": "application/json"
      })
  });
  let data = await response.json();

  //turn off spinner 
  if (response) {
    document.getElementById('spinner').style.display = 'none';
  };

  // remove any old data
  let previous_data = document.querySelectorAll('.results');
  for (let k=0;k<previous_data.length;k++) {
      previous_data[k].remove();
  };

  //set up header and table for results
  let table_div = document.querySelector('#predictions')
  let newHeader = document.createElement('h4');
  newHeader.textContent = "Results"
  let newAttribute = document.createAttribute('class')
  newAttribute.value = 'results'
  newHeader.setAttributeNode(newAttribute);
  table_div.appendChild(newHeader)

  //table
  let newTable = document.createElement('table')
  let newAttribute2 = document.createAttribute('class')
  newAttribute2.value = 'results table table-responsive'
  newTable.setAttributeNode(newAttribute2);
  table_div.appendChild(newTable)     
          
  //table head
  let newThead = document.createElement('thead');
  let newAttribute3 = document.createAttribute('class');
  newAttribute3.value = 'thead-light results';
  newThead.setAttributeNode(newAttribute3);
  let table_overall = document.querySelector('.table');
  table_overall.appendChild(newThead);

  //table row for table header
  let newTrow = document.createElement('tr');
  let table_head = document.querySelector('.thead-light');
  table_head.appendChild(newTrow);

  //table header cell 1
  let newTh1 = document.createElement('th');
  newTh1.textContent = 'Machine Learning Model';
  let newAttribute5 = document.createAttribute('scope');
  newAttribute5.value = 'col';
  newTh1.setAttributeNode(newAttribute5);
  let table_row = document.querySelector('tr')
  table_row.appendChild(newTh1);

  //table header cell 2
  let newTh2 = document.createElement('th');
  newTh2.textContent = 'Edibility Prediction';
  let newAttribute6 = document.createAttribute('scope');
  newAttribute6.value = 'col';
  newTh2.setAttributeNode(newAttribute6);
  table_row.appendChild(newTh2);

  //table body
  let newTbody = document.createElement('tbody');
  let newAttribute4 = document.createAttribute('class');
  newAttribute4.value = 'results';
  newTbody.setAttributeNode(newAttribute4);
  table_overall.appendChild(newTbody);



  //break off two pieces from data for table
  let table_info = (({amodelName, bmodelPrediction}) => ({amodelName, bmodelPrediction}))(data);
 
  //select location to insert data
  tBody = document.querySelector('tbody'); 

  //table with model name & prediction
  for (let i=0;i<5;i++){ //5 models = 5 rows
      let newtr = document.createElement('tr');
      newtr.setAttribute('class','results'); //new row class
      for (const value of Object.values(table_info)) {
          let newtd = document.createElement('td');
          let newAtt = document.createAttribute('class')
          //new class for cell
          if (value[i] == 1) {
            newtd.textContent = 'yes, edible' //add data to cell
            newAtt.value = 'table-success results';
          } else if (value[i] == 0) {
            newtd.textContent = 'no, inedible' //add data to cell
            newAtt.value = 'table-danger results';
          } else {
            newtd.textContent = value[i] //add data to cell
            newAtt.value = 'results';
          };
          newtd.setAttributeNode(newAtt);
          newtr.appendChild(newtd); // add new cell to new row
      };
      tBody.appendChild(newtr); // add new row to tbody
  };



  // chart of scores--reverse makes chart match order of table
  let models = (data.amodelName).reverse();
  let accuracyScores = (data.cmodelAccuracy).reverse();
  let precisionScores = (data.emodelPrecision).reverse();
  let f1Scores = (data.dmodelF1).reverse();
  let recallScores = (data.fmodelRecall).reverse();
  
  let trace1 = {
    type: 'scatter',
    x: accuracyScores,
    y: models,
    mode: 'markers',
    name: 'Accuracy',
    marker: {
      color: 'rgb(27,158,119)',
      line: {
        color: 'rgba(156, 165, 196, 1.0)',
        width: 1,
      },
      opacity: 0.6,
      symbol: 'circle',
      size: 16
    }
  };

  let trace2 = {
    x: f1Scores,
    y: models,
    mode: 'markers',
    name: 'F1',
    marker: {
      color: 'rgb(217,95,2)',
      line: {
        color: 'rgba(217, 217, 217, 1.0)',
        width: 1,
      },
      opacity: 0.6,
      symbol: 'circle',
      size: 16
    }
  };
  
  let trace3 = {
    x: precisionScores,
    y: models,
    mode: 'markers',
    name: 'Precision',
    marker: {
      color: 'rgb(117,112,179)',
      line: {
        color: 'rgba(217, 217, 217, 1.0)',
        width: 1,
      },
      opacity: 0.6,
      symbol: 'circle',
      size: 16
    }
  };

  let trace4 = {
    x: recallScores,
    y: models,
    mode: 'markers',
    name: 'Recall',
    marker: {
      color: 'rgb(231,41,138)',
      line: {
        color: 'rgba(217, 217, 217, 1.0)',
        width: 1,
      },
      opacity: 0.6,
      symbol: 'circle',
      size: 16
    }
  };

  let plot_data = [trace1, trace2, trace3, trace4];
  
  let layout = {
    title: 'Evaluation scores per model',
    xaxis: {
      showgrid: false,
      showline: true,
      linecolor: 'rgb(102, 102, 102)',
      tickfont: {
        font: {
          color: 'rgb(102, 102, 102)'
        }
      },
      autotick: true,
      tickcolor: 'rgb(102, 102, 102)',
      ticks: 'outside',
      hoverformat: '.3f' //when hovering, data points rounded to 3 decimal places
    },
    margin: {
      l: 160,
      r: 40,
      b: 50,
      t: 80
    },
    legend: {
      font: {
        size: 12,
      },
      y: 4,
      xanchor: 'right'
    },
    paper_bgcolor: 'rgb(254, 247, 234)',
    plot_bgcolor: 'rgb(254, 247, 234)',
    hovermode: 'closest'
  };
  
  let config = {
    responsive: true, 
    modeBarButtonsToRemove: ['zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d','resetScale2d', 'toggleSpikelines']
  };

  Plotly.newPlot('scores', plot_data, layout, config);

};