// Sample modal functions
function openModal() {
  document.getElementById("modalOverlay").style.display = "none";
}
function CreateJobModal(title,width = '0',height = '0') {
  const overlay = document.getElementById("modalOverlay");
  const modalTitle = document.getElementById("modalTitle");
  const modalContent = document.getElementById("modalContent");
  const modelFrame = document.querySelector(".modal-frame");

  modalTitle.textContent = title;
  // modalContent.innerHTML = content;
  overlay.style.display = "flex";
  document.getElementById("job-submit").value='';
  document.getElementById("btn-secondary").click();

  // modelFrame.style.width = width;
  // modelFrame.style.height = height;
}

// Sample custom-modal functions
function CreateUserModal(title,overlayid,headertitleid) {
  const overlay = document.getElementById(overlayid);
  const modalTitle = document.getElementById(headertitleid);

  modalTitle.textContent = title;
  overlay.style.display = "flex";
  document.getElementById('addeduser').innerText = "Add User";
  document.getElementById('addeduser').value = "";
  document.getElementById("btn-secondary2").click();
  document.getElementById('pass-req').required = true;
  document.getElementById('repass-req').required = true;
}
function openUserModal(overlayid) {
  document.getElementById(overlayid).style.display = "none";
}

document.getElementById('jobForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = e.target;
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());
  document.getElementById('job-submit').disabled=true;
  
  // Convert numeric fields to numbers
  data.batch = parseInt(data.batch);
  data.sems = data.sems ? parseInt(data.sems) : null;
  data.Backlogs = data.Backlogs?parseInt(data.Backlogs) : 0;
  data.cgpa_value = data.cgpa_value ? parseFloat(data.cgpa_value) : null;

  let adminame=document.getElementById("logout1").textContent.trim();
  data.posted_by=adminame;
  data.department = [];
  document.querySelectorAll("input[name='department']:checked").forEach((checkbox) => {
    data.department.push(checkbox.value);
  });
  
  let endpoint = 'create-job'
  let method_To = 'POST';
  let jobid = document.getElementById("job-submit").value;

  if (jobid !== '') {
    console.log(jobid);
    endpoint= `updatejob/${jobid}`;
    method_To = 'PUT';
  }
  try {
      const response = await fetch(`/${endpoint}`, {
          method: method_To,
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
      });

      const responseData = await response.json();

      if (!response.ok) {
          let errorMessage = 'Error: ';
          if (responseData.detail) {
              // Handle validation errors
              errorMessage += responseData.detail.map(err => 
                  `${err.loc[1]} ${err.msg}`).join(', ');
          } else {
              errorMessage += 'Submission failed';
          }
          alert(errorMessage);
          return;
      }
      alert(responseData.message);
      // form.reset(); // Clear form
      // Optionally redirect: window.location.href = '/success/';
  } catch (error) {
      console.error('Error:', error);
      alert('Network error - Please try again.');
  }

  finally{
    document.getElementById('job-submit').disabled=false;
    if (jobid != '') {
      document.getElementById('modalOverlay').style.display = "none";
      // document.getElementById("close1").click();
      // document.getElementById("close3").click();
      document.getElementById("job-card1").click();
    }
  }

});

document.getElementById('userform').addEventListener('submit',async (e) => {
  e.preventDefault();
  addbtn = document.getElementById('addeduser');
  addbtn.disabled = true;
  addbtn.textContent = "Submitting...";
  const form = e.target;
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  data.backlog = parseInt(data.backlog);
  data.sem = parseInt(data.sem);
  data.phone = parseInt(data.phone);
  data.passout = parseInt(data.passout);
  data.cgpa = parseFloat(data.cgpa);
  console.log(data);
  console.log(formData);
  let userbtnid=document.getElementById('addeduser').value;
  console.log(userbtnid);
  let endpoint = 'add-user';
  let method_To = 'POST';
  if (userbtnid !== '') {
    endpoint= `updateuser/${userbtnid}`;
    method_To = 'PUT';
  }

  try {
    let response = await fetch('/'+endpoint,{
      method: method_To,
      headers: {
        'Content-Type': 'application/json',
    },
      body: JSON.stringify(data)
    });

    let responseData = await response.json();
    // console.log(response);
    // console.log(responseData);
    if (!response.ok){
      alert("Error.v1: "+responseData.detail);
      addbtn.disabled = false;
      addbtn.textContent = "Add User";
      return;
    }
    else{
      alert(responseData.message);
      addbtn.disabled = false;
      addbtn.textContent = "Add User";
      return;
    }
  } catch (error) {
    addbtn.disabled = false;
    addbtn.textContent = "Add User";
    alert("Error.v2: "+error)
  }

  finally{
    if (userbtnid != '') {
      document.getElementById('modalOverlay').style.display = "none";
      document.getElementById("user-card1").click();
    }
  }
});

async function getalljobs() {
  try {
    let response = await fetch('/getpostedjobs');
    let data = response.json()
    return data
    
  } catch (error) {
    alert('error3: ',error);
  }
}

async function getallusers() {
  try {
    let response = await fetch('/show');
    let data = response.json()
    return data
    
  } catch (error) {
    alert('error3: ',error);
  }
}

async function getlist(bool) {
  let data;
  try {
    if (bool == true) {
      data = await getalljobs();
      let content = `<div class="job-list" id="jobList">
      </div>`;
      let content_part = document.getElementById("commonContent");
      content_part.innerHTML = content;
      let joblist = document.getElementById("jobList");
      data.forEach((element) => {
        joblist.innerHTML += `<div class="job-element">
        <div class="job-info">
        <span class="job-name">Id ${element["id"].slice(-4)}. ${element["company"]}, ${element["role"]}</span>
        <span class="job-meta">${element["skills"]}</span>
        <span class="job-meta">Posted on: ${element["posted_on"]}</span>
        </div>
        <div class="job-actions">
        <span class="update-icon2" data-value="${element["id"]}" >Edit</span>
        <span class="delete-icon2" data-value="${element["id"]}" >Delete.</span>
        </div>
        </div> `;
      });
      return data;
    }
    else {
      data = await getallusers();
      let content = `<div class="job-list" id="jobList">
      </div>`;
      let content_part = document.getElementById("commonContent");
      content_part.innerHTML = content;
      let joblist = document.getElementById("jobList");
      data.forEach((element) => {
        joblist.innerHTML += `<div class="job-element">
        <div class="job-info">
        <span class="job-name">Id ${element["id"].slice(-4)}. ${element[
          "name"
        ].toUpperCase()}</span>
        <span class="job-meta">${element["usn"]}</span>
        </div>
        <div class="job-actions">
        <span class="update-icon2" data-value="${element["id"]}" >Edit</span>
        <span class="delete-icon2" data-value="${element["id"]}" >Delete.</span>
        </div>
        </div> `;
      });
      return data;
    }
  } 
  catch (error) {
    alert("error" + error);
  }
}
  
async function removejob(jobid,btn) {
  await fetch(`/deletejob?jobid=${jobid}`, {
    method: 'POST'
  }).then(response =>{
    if (!response.ok){
      throw new Error("Error deleting job");
    }
    else{
      alert('Job Deletion successful.'); 
      btn.parentElement.parentElement.remove();
    }

  
  }).catch(err =>{
    alert(err);
    
  });
}
async function removeuser(userid,btn) {
  await fetch(`/softdeleteuser?userid=${userid}`, {
    method: 'POST'
  }).then(response =>{
    if (!response.ok){
      throw new Error("Error deleting user");
    }
    else{
      alert('User Deletion successful.'); 
      btn.parentElement.parentElement.remove();
    }

  
  }).catch(err =>{
    alert(err);
    
  });
}

async function updatejob(data,index) {
  document.getElementById('commonOverlay').style.display = "none";
  const overlay = document.getElementById("modalOverlay");
  const modalTitle = document.getElementById("modalTitle");
  modalTitle.textContent = "Update Job";
  overlay.style.display = "flex";
  let realdata = data[index];
  document.getElementById('company-field').value = realdata.company;
  document.getElementById('role-field').value = realdata.role;
  document.getElementById('cgpaop-field').value = realdata.cgpa_operator;
  document.getElementById('cgpa-field').value = realdata.cgpa_value;
  document.getElementById('blog-field').value = realdata.backlog_allowed;

  const checkboxes = document.querySelectorAll('.deptCheck');
  checkboxes.forEach(checkbox => {
    checkbox.checked = realdata.department_req.includes(checkbox.value);
  });

  document.getElementById('batch-field').value = realdata.batch;
  document.getElementById('skill-field').value = realdata.skills;
  document.getElementById('sem-field').value = realdata.sem_completed;
  document.getElementById('applyby-field').value = realdata.apply_by;
  document.getElementById('applyl-field').value = realdata.apply_link;
  document.getElementById('description-field').value = realdata.description;
  document.getElementById("job-submit").value = realdata.id;
  
  
}

async function updateuser(data,index) {
  CreateUserModal('Update User','userOverlay','headerTitle');
  openUserModal('commonOverlay');
  let realdata = data[index];
  document.getElementById('sno-field').value = realdata.sno;
  document.getElementById('usn-field').value = realdata.usn;
  document.getElementById('name-field').value = realdata.name;
  document.getElementById('gender-field').value = realdata.gender;
  document.getElementById('phone-field').value = realdata.phone;
  document.getElementById('email-field').value = realdata.email;
  // document.getElementById('dept-field').value = realdata.dept;
  document.querySelectorAll(".deptRadio").forEach(radio=>{
    if (radio.value==realdata.dept){
      radio.checked = true;
    }
  })

  document.getElementById('semuser-field').value = realdata.sem;
  document.getElementById('passout-field').value = realdata.passout;
  document.getElementById('skills-field').value = realdata.skills;
  document.getElementById('cgpauser-field').value = realdata.cgpa;
  document.getElementById('backlog-field').value = realdata.backlog;
  document.getElementById('adminR-field').value = realdata.admin_remark;
  document.getElementById('addeduser').value = realdata.id;
  document.getElementById('pass-req').required = false;
  document.getElementById('repass-req').required = false;
  // document.getElementById('addeduser').innerText = "Update";

}

// false fetches users list,truth -> jobslist
document.getElementById('job-card1').addEventListener('click',async (e) => {
  const data =await getlist(true);
  
  document.querySelectorAll(".delete-icon2").forEach(btn => {
    btn.addEventListener('click',async () => {
      try {
        await removejob(btn.dataset.value,btn)
        
      } catch (error) {
        alert("Job_deletion error: "+error);
      }
    }) 
  });

  document.querySelectorAll(".update-icon2").forEach(btn => {
    btn.addEventListener('click',async () => {
      try {
        let index = data.findIndex(dat => dat.id===btn.dataset.value);
        await updatejob(data,index);
      } catch (error) {
        alert("Job_update error: "+error);
      }
    }) 
  });

})

document.getElementById('user-card1').addEventListener('click',async (e) => {
  const data = await getlist(false);
  console.log(data);
  document.querySelectorAll(".delete-icon2").forEach(btn => {
      btn.addEventListener('click',async () => {
        try {
          await removeuser(btn.dataset.value,btn)
          
        } catch (error) {
          alert("User_deletion error: "+error);
        }
      });
  });

  document.querySelectorAll(".update-icon2").forEach(btn => {
    btn.addEventListener('click',async () => {
      try {
        let index = data.findIndex(dat => dat.id===btn.dataset.value);
        await updateuser(data,index);
      } catch (error) {
        alert("User_update error: "+error);
      }
    }) 
  });


})
// Send notification pure js===========
async function toggleField(radio) {
    document.querySelectorAll(".recInputs").forEach(element => {
        element.value='';
        element.disabled = true;
    });

    if (radio.value === 'or') {
        document.getElementById(radio.value+'mode1').disabled=false;
        document.getElementById(radio.value+'mode2').disabled=false;

        document.getElementById(radio.value+'mode1sem').disabled=false;
        document.getElementById(radio.value+'mode2sem').disabled=false;
        document.getElementById(radio.value+'mode1gender').disabled=false;
        document.getElementById(radio.value+'mode2gender').disabled=false;
        document.getElementById(radio.value+'mode1dept').disabled=false;
        document.getElementById(radio.value+'mode2dept').disabled=false;
    }
    else if(radio.value ==='and'){
        document.getElementById(radio.value+'mode1').disabled=false;
        document.getElementById(radio.value+'mode2').disabled=false;

        document.getElementById(radio.value+'mode1sem').disabled=false;
        document.getElementById(radio.value+'mode2sem').disabled=false;
        document.getElementById(radio.value+'mode1gender').disabled=false;
        document.getElementById(radio.value+'mode2gender').disabled=false;
        document.getElementById(radio.value+'mode1dept').disabled=false;
        document.getElementById(radio.value+'mode2dept').disabled=false;
    }
    else {
        document.getElementById(radio.value+'mode').disabled=false;
    }
    // document.getElementById(radio.value+'mode1').disabled=false;
    // document.getElementById(radio.value+'mode2').disabled=false;
    // document.getElementById(radio.value+'mode').disabled=false;
}

async function presentpane(params) {
    
    // let other_val = ['sem','gender','dept']
    document.getElementById(params.id+'sem').style.display = 'none';
    document.getElementById(params.id+'dept').style.display = 'none';
    document.getElementById(params.id+'gender').style.display = 'none';

    let val= params.value;
    document.getElementById(params.id+val).style.display = 'inline-block';
}
// Send notification pure js===========end

document.getElementById('msg-card1').addEventListener('click',async (e) => {
  content = `<div class="outerlayout">
        <form id="msgForm">
            <div class="optionpane">
                <label for="options">Select Reciepients</label>
                <div class="orpane">
                    <input type="radio" name='options' value="or" onclick="toggleField(this)" required>
                    <select name="mode1" class="recInputs" id="ormode1" onchange="presentpane(this)" disabled>
                        <option value="--">--</option>
                        <option value="sem">Semester</option>
                        <option value="dept">dept</option>
                        <option value="gender">gender</option>
                    </select>
                    <select name="orsem1" class="recInputs subrinp" id="ormode1sem" style="display: none;">
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                        <option value="5">5</option>
                        <option value="6">6</option>
                        <option value="7">7</option>
                        <option value="8">8</option>
                    </select>
                    <select name="ordept1" class="recInputs subrinp" id="ormode1dept" style="display: none;">
                        <option value="CSE">CSE</option>
                        <option value="CSE-AIML">CSE-AIML</option>
                        <option value="EC">EC</option>
                        <option value="EEE">EEE</option>
                        <option value="Mech">Mechanical</option>
                        <option value="Civil">Civil</option>
                    </select>
                    <select name="orgender1" class="recInputs subrinp" id="ormode1gender" style="display: none;">
                        <option value="male">male</option>
                        <option value="female">female</option>
                        <option value="idk">idk</option>
                    </select>
                    OR
                    <select name="mode2" class="recInputs" id="ormode2" onchange="presentpane(this)" disabled>
                        <option value="--">--</option>
                        <option value="sem">Semester</option>
                        <option value="dept">dept</option>
                        <option value="gender">gender</option>
                    </select>
                    <select name="orsem2" class="recInputs subrinp" id="ormode2sem" style="display: none;">
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                        <option value="5">5</option>
                        <option value="6">6</option>
                        <option value="7">7</option>
                        <option value="8">8</option>
                    </select>

                    <select name="ordept2" class="recInputs subrinp" id="ormode2dept" style="display: none;">
                        <option value="CSE">CSE</option>
                        <option value="CSE-AIML">CSE-AIML</option>
                        <option value="EC">EC</option>
                        <option value="EEE">EEE</option>
                        <option value="Mech">Mechanical</option>
                        <option value="Civil">Civil</option>
                    </select>

                    <select name="orgender2" class="recInputs subrinp" id="ormode2gender" style="display: none;">
                        <option value="male">male</option>
                        <option value="female">female</option>
                        <option value="idk">idk</option>
                    </select>
    
                </div>
                <div class="andpane">
                    <input type="radio" name='options' value="and" onclick="toggleField(this)">
                    <select name="mode1" class="recInputs" id="andmode1" onchange="presentpane(this)" disabled>
                        <option value="--">--</option>
                        <option value="sem">Semester</option>
                        <option value="dept">dept</option>
                        <option value="gender">gender</option>
                    </select>
                    <select name="andsem1" class="recInputs subrinp" id="andmode1sem" style="display: none;">
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                        <option value="5">5</option>
                        <option value="6">6</option>
                        <option value="7">7</option>
                        <option value="8">8</option>
                    </select>
                    <select name="anddept1" class="recInputs subrinp" id="andmode1dept" style="display: none;">
                        <option value="CSE">CSE</option>
                        <option value="CSE-AIML">CSE-AIML</option>
                        <option value="EC">EC</option>
                        <option value="EEE">EEE</option>
                        <option value="Mech">Mechanical</option>
                        <option value="Civil">Civil</option>
                    </select>
                    <select name="andgender1" class="recInputs subrinp" id="andmode1gender" style="display: none;">
                        <option value="male">male</option>
                        <option value="female">female</option>
                        <option value="idk">idk</option>
                    </select>
                    AND
                    <select name="mode2" class="recInputs" id="andmode2" onchange="presentpane(this)" disabled>
                        <option value="--">--</option>
                        <option value="sem">Semester</option>
                        <option value="dept">dept</option>
                        <option value="gender">gender</option>
                    </select>
                    <select name="andsem2" class="recInputs subrinp" id="andmode2sem" style="display: none;">
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                        <option value="5">5</option>
                        <option value="6">6</option>
                        <option value="7">7</option>
                        <option value="8">8</option>
                    </select>
                    <select name="anddept2" class="recInputs subrinp" id="andmode2dept" style="display: none;">
                        <option value="CSE">CSE</option>
                        <option value="CSE-AIML">CSE-AIML</option>
                        <option value="EC">EC</option>
                        <option value="EEE">EEE</option>
                        <option value="Mechanical">Mechanical</option>
                        <option value="Civil">Civil</option>
                    </select>
                    <select name="andgender2" class="recInputs subrinp" id="andmode2gender" style="display: none;">
                        <option value="male">male</option>
                        <option value="female">female</option>
                        <option value="idk">idk</option>
                    </select>
                </div>
                <div class="custompane">
                    <input type="radio" name='options' value="msg" onclick="toggleField(this)">
                    <input type="text" name='usnlist' class="recInputs" id="msgmode" disabled required>
                </div>
            </div>
            <div class="msgpane">
                <label for="message">Write your message</label>
                <textarea name="message_area" id="msgarea" required></textarea>
                <button type="submit" id='msgsubmit'>Send</button>
                <button type="reset" id='resetbtn' >Clear</button>
            </div>
        </form>
    </div>`;
  document.getElementById('commonContent').innerHTML=content;
  document.getElementById('msgForm').addEventListener('submit',async e => {
    e.preventDefault();
    const form = e.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    console.log(JSON.stringify(data));
    try {
      let response = await fetch('/sendnotification',{
        method:'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body:JSON.stringify(data)
      });

      const responseData = await response.json();

      if(!response.ok){
        alert("Error_L1: "+responseData.message);
        return;
      }
      else{
        alert(responseData.message);
        return;
      }
    } catch (error) {
      alert(error);
    }
    
  })
})



// Sample chart implementation
// You would typically use a charting library here

// This is just a placeholder

const chartContainer = document.getElementById("analytics-chart");
// chartContainer.innerHTML =
//   '<div style="background: #f1f5f9; height: 100%; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #64748b;">Analytics Chart</div>';

async function loadSkillsChart() {
  const response = await fetch('/testingMetrics');
  const data = await response.json();
  const response2 = await fetch('/get2ndgraph');
  const data2 = await response2.json();
  console.log(data);

  const ctx = document.getElementById('skillsChart').getContext('2d');
  
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: Object.keys(data),
      datasets: [
        {
          label: 'Skill Count',
          data: Object.values(data).map(item => item[0]),
          backgroundColor: 'rgba(54, 162, 235, 0.6)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        },
        {
          label: 'User Count',
          data: Object.values(data).map(item => item[1]),
          backgroundColor: 'rgba(255, 99, 132, 0.6)',
          borderColor: 'rgba(255,99,132,1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Counts'
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: 'Top 3 Skills vs Users'
        }
      }
    }
  });


  const ctx2 = document.getElementById('skillsChart2').getContext('2d');

  // Create a bar chart with the fetched data
  new Chart(ctx2, {
    type: 'bar',
    data: {
      labels: Object.keys(data2), // Semester labels (6, 7, 8)
      datasets: [{
        label: 'Cumulative Count',
        data: Object.values(data2), // Cumulative counts for each semester
        backgroundColor: 'rgba(54, 162, 235, 0.6)', // Bar color
        borderColor: 'rgba(54, 162, 235, 1)', // Border color
        borderWidth: 1,
        barThickness: 60
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Count of Records'
          }
        }
      },
      plugins: {
        title: {
          display: true,
          text: 'Cumulative Counts for Semesters 6, 7, 8'
        }
      }
    }
  });

}

// loadSkillsChart()
loadSkillsChart();


function logout() {
  fetch("/admin_logout", {
    method: "POST",
    credentials: "same-origin", // Ensures cookies are sent
  }).then((response) => {
    if (response.redirected) {
      window.location.href = response.url; // Redirect to login
    }
  });
}
