const matrix = document.querySelector("#matrix")
const objinp = document.querySelector("#objinp")
const ansDiv = document.querySelector("#ans")


const createMatrix = (row, col) => {
    matrix.innerHTML = "";
    for(let i = 0; i < row; i++){
        for(var j = 0; j < col; j++){
            let inp = document.createElement("input")
            // inp.type = "number"
            inp.innerText = " "
            inp.id = `cell${i}${j}`
            inp.classList.add('cell')
            matrix.appendChild(inp)
            matrix.appendChild(document.createTextNode(`x${j+1}`))
        }
        let inq  = document.createElement("select")
        inq.id = `cell${i}${j}`

        let lopt = document.createElement("option")
        lopt.setAttribute( 'value', '<=')
        lopt.innerText = '<='

        let eqlopt = document.createElement("option")
        eqlopt.setAttribute('value','=')
        eqlopt.innerText = '='

        let gopt = document.createElement("option")
        gopt.setAttribute('value', '>=')
        gopt.innerText = '>='

        inq.appendChild(lopt)
        inq.appendChild(eqlopt)
        inq.appendChild(gopt)

        let rhs = document.createElement("input")
        // rhs.type = "number"
        rhs.id = `cell${i}${j+1}`

        matrix.appendChild(inq)
        matrix.appendChild(rhs)
        matrix.appendChild(document.createElement("br"))
        
    }
}

const createZ = (col) => {
    objinp.innerHTML = `<select name="type" id="max-min">
            <option value="1">Max</option>
            <option value="2">Min</option>
        </select>`;
    
    for(let cell = 1; cell <= col; cell++){
        let inp = document.createElement("input")
        // inp.type = "number"
        inp.classList.add('zobj')
        objinp.appendChild(inp)
        objinp.appendChild(document.createTextNode(`x${cell}`))
    }
}


document.querySelector("#makematrix").addEventListener('click', ()=>{
    let col = document.querySelector("#totalvar").value;
    let row = document.querySelector("#totalcons").value;
    
    createZ(col)
    createMatrix(row, col)
})

createZ(2)
createMatrix(2, 2)


document.querySelector("#submit").addEventListener('click', async(e) =>{
    e.preventDefault();

    let totalvar = Number(document.querySelector("#totalvar").value);
    let totalcons = Number(document.querySelector("#totalcons").value);
    let objZ = []
    let Z = document.querySelector("#objinp").children;
    for(let i = 1; i < Z.length; i++){
        objZ.push(Number(Z[i].value))
    }
    console.log(objZ)
    console.log(totalvar, totalcons+1)
    let matrix = [];
    let countgreat = 0;
    for(let i=0; i < totalcons; i++){
        let temp = []
        for(let j=0; j < (totalvar + 2) ; j++){
            console.log(`#cell${i}${j}`)
            temp.push(document.querySelector(`#cell${i}${j}`).value)
        }
        if(temp.includes('>=')){
            countgreat += 1
        }
        console.log('nikit')
        matrix.push(temp)
    }
    console.log(matrix)
    console.log("count", countgreat)

    const type = document.querySelector("#max-min").value;
    console.log(type)

    ansDiv.innerText = "Loading...";

    const result = await fetch('/calc',{
        method : 'POST',
        headers: {'Content-Type': 'application/json'},
        body : JSON.stringify({
            totalvar,
            totalcons,
            objZ,
            matrix,
            countgreat,
            type
        })
    }).then(res => res.json())
    console.log(result)
    ansDiv.innerText = result.data;
})


// setInterval(() =>{
//     location.reload()
//     console.log('refreshing')
// }, 100)