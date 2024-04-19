const app = require("express")();
const { spawn } = require('child_process');
const { PythonShell } = require('python-shell');

function runMainQrCode() {
    return new Promise(async function (resolve, reject) {
        let r = await runPy()
        console.log(JSON.parse(JSON.stringify(r.toString())), "Done...!@")
    })
}

async function runServerPy() {
    let r = await new Promise(function (resolve, reject) {
        let options = {
            mode: 'text',
            pythonOptions: ['-u'],
            scriptPath: './', // Path to your script
        };

        PythonShell.run('server.py', options, function (err, results) {
            if (err) throw err;
            console.log('results: ');
            for (let i of results) {
                console.log(i, "---->", typeof i)
            }
            resolve(results[1])
        });
    });
    console.log(JSON.parse(JSON.stringify(r.toString())), "Done...!@");
}

const PORT = 7777;

app.listen(PORT, () => {
    console.log(`its alive on https://localhost:${PORT}`);
    runServerPy();
});

app.get('/', function (req, res) {
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python', [__dirname + '/python_code.py']);
    res.sendFile(__dirname + '/index.html');
});
