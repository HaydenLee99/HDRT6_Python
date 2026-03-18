const btnJikwon = document.querySelector("#btnJikwon");
const btnOne = document.querySelector("#btnOne");
const btnBuser = document.querySelector("#btnBuser");
const btnDept = document.querySelector("#btnDept");

const jikwonno = document.querySelector("#jikwonno");
const buserno = document.querySelector("#buserno");

const msg = document.querySelector("#msg");
const thead = document.querySelector("#thead");
const tbody = document.querySelector("#tbody");

function setMsg(text){
    msg.textContent = text;
}

function clearTable(){
    thead.innerHTML="";
    tbody.innerHTML="";
}

function makeTable(rows){
    clearTable();

    if(!rows || rows.length === 0){
        setMsg("자료 없음");
        return;
    }

    let header = "<tr>";

    Object.keys(rows[0]).forEach(key=>{
        header += "<th>" + key + "</th>";
    });
    header += "</tr>";
    thead.innerHTML = header;

    rows.forEach(r=>{
        let tr = "<tr>"
        Object.values(r).forEach(v=>{
            tr += "<td>" + v + "</td>";
        });
        tr += "</tr>";
        tbody.innerHTML += tr;
    });
}

// 전체 직원 조회
async function loadJikwon() {
    const res = await fetch("/api/jikwon");
    const mydata = await res.json();
    makeTable(mydata.data);

    setMsg("전체 직원 조회 완료");
}
btnJikwon.onclick = loadJikwon;

// 직원 일부 조회
async function loadOne() {
    const no = jikwonno.value;
    const res = await fetch("/api/jikwon/" + no);
    const mydata = await res.json();
    makeTable([mydata.data]);

    setMsg("직원 1명 조회 완료");
}
btnOne.onclick = loadOne;


// 전체 부서 조회
async function loadBuser() {
    const res = await fetch("/api/buser");
    const mydata = await res.json();
    makeTable(mydata.data);

    setMsg("전체 부서 조회 완료");
}
btnBuser.onclick = loadBuser;

// 부서 직원 조회
async function loadDept() {
    const bno = buserno.value;
    const res = await fetch("/api/buser/" + bno);
    const mydata = await res.json();
    makeTable(mydata.data);

    setMsg("부서 직원 조회 완료");
}
btnDept.onclick = loadDept;