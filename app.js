var mysql = require('mysql');
var express = require('express');
var bodyParser = require('body-parser');
const path = require('path');
var request = require('request');

var port = 8080;

var connection = mysql.createConnection({
	host     : '195.224.157.110',
	user     : 'remote',
	password : 'Lee2391e@s',
	database : 'hmmpi'
});

var app = express();

app.set('view engine', 'ejs');
app.use(express.static("public"));

app.use(bodyParser.urlencoded({extended : true}));
app.use(bodyParser.json());

app.get('/', function(res, req){
    response.sendFile(path.join(__dirname + '/public/index.html'));
});

app.post('/similarity', function(req, res){

	const data = {
		search: req.body.search,
	};

	var clientServerOptions = {
		uri: 'http://localhost:5000/similarity',
		body: JSON.stringify(data),
		method: 'POST',
		async: false,
		headers: {
			'Content-Type': 'application/json'
		}
	}
	request(clientServerOptions, function(error, response) {
		res.end(response.body);
		//res.end(JSON.stringify(response.body));
	});
});

/*
app.post('/search', function (req, res){
    let search = req.body.search;
	console.log(search);
	connection.query('select distinct itsm_ref, itsm_summary, itsm_description from itsm_master where match(itsm_summary, itsm_description) against (?) AND itsm_ref like "HSD%" limit 50', [search], function(err, rows, fields) {
        if (err) throw err;
		if(rows.length>0){
			res.end(JSON.stringify(rows));
		}
		else {
			res.end(JSON.stringify('Nodata'));
		}
	});
});

app.get('/show', function(req, res){
    let id = req.query.id;
	res.render('view', { id: id });
});

app.post('/feedback', function(req, res){
    let id = req.body.id;
	connection.query('select distinct itsm_comments from itsm_comments where itsm_ref = ?', [id], function(err, rows, fields) {
        if (err) throw err;
		if(rows.length>0){
			res.end(JSON.stringify(rows));
		}
		else {
			res.end(JSON.stringify('Nodata'));
		}
	});
});

app.post('/attached', function(req, res){
    let id = req.body.id;
	connection.query('select * from itsm_attachments where itsm_ref = ?', [id], function(err, rows, fields) {
        if (err) throw err;
		if(rows.length>0){
			res.end(JSON.stringify(rows));
		}
		else {
			res.end(JSON.stringify('Nodata'));
		}
	});
});
*/

app.listen(port);
console.log("Runnging at port 8080");