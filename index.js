const spawn = require('child_process').spawn
const express = require('express')
const cors = require('cors')
require('dotenv').config()
const app = express()
app.use(express.json())
app.use(cors());
app.use('/',express.static('static'))
app.use(express.urlencoded({ extended: true }));
const PORT = 3001

app.post('/calc', (req, res) => {
    console.log(req.body)
    const {totalvar, totalcons, objZ, matrix, countgreat, type} = req.body;
    const process = spawn('python', ['./revised-simplex.py', totalvar, totalcons, JSON.stringify(objZ), JSON.stringify(matrix), countgreat, type])
    var dataToSend = ""
    process.stdout.on('data', (data)=>{
    //     // console.log(data.toString())
        // dataToSend += data.toString()
    //     console.log(data.toString())
    //     // res.status(200).json({status : 200, data : dataToSend})
    //     // res.send({data : data.toString()})
    //     return res.status(200).json({status : (200), data : data.toString()})
        // console.log(data.toString())
        dataToSend += data.toString()
    })
    process.stdout.on('close', () => {
        console.log(dataToSend)
        res.status(200).json({status : 'ok',data: dataToSend})
    })

})


app.listen(process.env.PORT || PORT, ()=>{
    console.log('good boi')
})