async function logout() {
  fetch("/logout", {
    method: "POST",
    credentials: "same-origin", // Ensures cookies are sent
  }).then((response) => {
    if (response.redirected) {
      window.location.href = response.url; // Redirect to login
    }
  });
}

const ids = [];

async function fetchfilteredjobs() {
  // let response =await fetch("http://127.0.0.1:8000/fetchfilteredjobs");
  let response =await fetch("/fetchfilteredjobs");
  // let jobs_got = response.json();
  // console.log(response.json());
  return response.json();
}
fetchfilteredjobs().then(result=> {
  let jobsfiltered = result['filtered'];
  let filtered_match_P = result['match_percent_filtered'];

  ids.push(...Object.keys(filtered_match_P));
  // console.log(ids)

  // console.log((jobsfiltered));
  // console.log((filtered_match_P));
  let jobContainer = document.getElementById("alerts-container");

  jobContainer.innerHTML='';

  jobsfiltered.forEach(job => {
    
    let matchPerc_job = filtered_match_P[job.id]
    
    let tier='';
    
    if (matchPerc_job >=80 && matchPerc_job<=100 ){
      tier = "tier1";
      matchPerc_job +='%';
    }else if (matchPerc_job==999){
      tier = "";
      matchPerc_job = 'Unavailable';
    }else if (matchPerc_job>=25){
      tier = "tier2";
      matchPerc_job +='%';
    }else{
      tier = "tier3";
      matchPerc_job +='%';
    }
    // console.log(matchPerc_job)
    let jobCard = `<div class="alert-card ${tier}">
                    <h4>${job.role}</h4>
                    <p>${job.company}</p>
                    <p id='skillscore'>Skill Compatibility ${matchPerc_job}</p>
                    <button style="margin-top: 10px;" id='btn-${job.id}' class="apply-btn">Apply Now</button>
                </div>`

                jobContainer.innerHTML+=jobCard;
               
  });

  jobsfiltered.forEach((job) => {
    let btnn = document.getElementById(`btn-${job.id}`);
    btnn.addEventListener("click",function (){
      openJobDetails(job);
    })
  })


}).catch(error => {
  alert(`AI based job Matching failed.You can refresh or continue using HireBridge`+error);
}).then(fetchalljobs);


async function fetchalljobs() {
  // let response = await fetch("http://127.0.0.1:8000/fetchalljobs");
  let response = await fetch("/fetchalljobs");
  let jobs_got = await response.json();
  // ?console.log(jobs_got)
  exclude_filterIds = ids
  exclude_filterIds.forEach(exIds => {
    jobs_got = jobs_got.filter(item => item.id !== exIds)
  });
  //  ?console.log(jobs_got)
  let jobContainer = document.getElementById("alerts-container-alljobs");
  jobContainer.innerHTML=''
  jobs_got.forEach(job => {
    // let jobString = JSON.stringify(job)
    let jobCard = `<div class="alert-card">
                    <h4>${job.role}</h4>
                    <p>${job.company}</p>
                    <button style="margin-top: 20px;" id='btn-${job.role}' class="apply-btn alertall">Apply Now</button>
                </div>`

                jobContainer.innerHTML+=jobCard;


                
  });

  jobs_got.forEach(job =>{
    let btn = document.getElementById(`btn-${job.role}`);
    btn.onclick=function(){
      openJobDetails(job);
    };
  })
  
}

let currUsername;

let fetching_profile=async () => {
  response = await fetch("/getcurruser");
  return response.json();
  
}
fetching_profile().then(data =>{
  // userinfo = JSON.parse(JSON.stringify(data));
  currUsername = data.name;
  let content = `<div class="hoga-kuch-toh">
  <p id="profile-sno">SNo. ${data.sno}</p>
  <p id="profile-sem" style="margin-right:10px">${data.sem} Sem</p>
  <p id="profile-batch">${data.passout} Batch</p> </div>
  <p id="profile-name">Name : ${data.name}</p>
  <p id="profile-usn">USN : ${data.usn}</p>
  <p id="profile-phone">Phone : ${data.phone}</p>
  <p id="profile-email">Email : ${data.email}</p>
  <p id="profile-dept">Department : ${data.department}</p>
  <p id="profile-skills">Skills : ${data.skills}</p>
  <p id="profile-cgpa">CGPA : ${data.cgpa}</p>
  <p id="profile-remak">Admin Remark : ${data.remark}</p>
  </div>
  <div class='changeP'>
  <span class="changeP-icon" id='changeP-iconbtn' >Change Password</span>
  </div>`;
  let profileModal = document.getElementById("profile_feature")
  profileModal.onclick = function() {
    openModal('Profile',content);
  }

  // let changeP_btn = document.getElementById("changeP-iconbtn");
  // changeP_btn.addEventListener('click',async (params) => {
  //   document.getElementById
  //   const res = await fetch('/changePssword');
  // })

  message_window = document.getElementById("chart-container")
  data.messages.forEach((element,index) => {
    message_window.innerHTML+= `<div class="msg-item">
        <span class="msg-name">${index+1}. ${element}</span>
        <div class="msg-actions">
          <span class="msgdelete-icon" data-value="${element}" >Delete.</span>
        </div>
      </div>`
  });
  // console.log(data.messages);

  document.querySelectorAll(".msgdelete-icon").forEach(element => {
    element.addEventListener("click",async (params) => {
      try {
        const value = params.target.getAttribute('data-value');
        // alert(data.usn);
        const response= await fetch(`/deletemsg?id=${data.usn}&message=${value}`,{
          method:'DELETE',
          headers:{
            'Content-Type': 'application/json',
          }
        });
        let response_data =await response.json();
        
        if(!response.ok){
          alert(response_data.detail);
          return
        }
        else{
          alert(response_data.message);
          element.parentElement.parentElement.remove();
        }
      } catch (error) {
        alert(error);
      }
    })
  });
  
  
})

async function ama_prompt() {
  let content = ` <div id="amainput">
    <input type="text" name="prompt" placeholder="Enter your prompt..." id="amatext">
    <button id="amabtn" type="button">submit</button>
  </div>
  <div id="amaresponse"></div>`
  const amaModal = document.getElementById("ama_feature")
  amaModal.onclick = async function() {
    openModal('Ask me Anything',content,'50%');
    let amabtn = document.getElementById('amabtn');
    let promptval = document.getElementById('amatext');
    let amaresponse = document.getElementById('amaresponse');
    let modalhead = document.getElementsByClassName('modal-frame');
    amabtn.onclick =async function(e){
      e.preventDefault();
      const ama = promptval.value;
      amabtn.disabled = true;
      amaresponse.innerHTML = '<div class="skeleton skeleton-card"></div>';
      await fetch('/gen2', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({prompt:ama})
      })
        .then(response => {
          if (!response.ok) {
            amaresponse.innerHTML = '';
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })

        // ["choices"][0]["message"]["content"]
        .then(data => {
          solution = data.choices[0].message.content;
          let formatted_sol = marked.parse(solution);
          amaresponse.innerHTML = formatted_sol;

        })
        .catch(error => {
          amaresponse.innerHTML = '';
          console.error('Error submitting data:', error);
        });

        amabtn.disabled = false;
    
  }
  }
  
}
ama_prompt();


async function res_gen_ai() {
  // userinfo=fetching_profile();
  let response=await fetch("/getcurruser");
  let userinfo =await response.json();
  //  ?console.log(userinfo);
  
  let content = `
  <div class="container">
  <form id="resumeUserForm">
        <label for="name">Name*</label>
        <input type="text" id="res_name" name="c_name" placeholder="Enter your name" value="${userinfo.name}" required>
        
        <label for="email">Email*</label>
        <input type="email" id="res_email" name="c_email" placeholder="Enter your email" value = "${userinfo.email}" required>
        
        <label for="phone">Phone*</label>
        <input type="text" id="res_phone" name="c_phone" placeholder="Enter your phone number" value="${userinfo.phone}" required>
        
        <label>College Education</label>
        <div class="row" id='edu'>
            <input type="text" id='lo' name="c_deg" placeholder="College Name" value="B.E ${userinfo.department} | KLS Vishwanathrao Deshpande Institute of Technology">
            <input type="text" name="c_degmarks" placeholder="CGPA" value="${userinfo.cgpa}">
            <input type="text" name="c_degbatch" placeholder="Batch" value="${userinfo.passout}">
        </div>
        
        <label>12th Education</label>
        <div class="row" id='edu'>
            <input type="text" name="c_coll" placeholder="12th School">
            <input type="text" name="c_collmarks" placeholder="%">
            <input type="text" name="c_collbatch" placeholder="Batch">
        </div>
        
        <label>Xth Education</label>
        <div class="row" id='edu'>
            <input type="text" name="c_school" placeholder="10th School">
            <input type="text" name="c_schoolmarks" placeholder="%">
            <input type="text" name="c_schoolbatch" placeholder="Batch">
        </div>
        
        <label for="skills">Skills</label>
        <input type="text" id="res_skills" name="c_skills" placeholder="Enter your skills" value="${userinfo.skills}">
        
        <label>Internship</label>
        <div class="row">
            <input type="text" name="c_int" placeholder="Internship Name">
            <input type="text" name="c_intdes" placeholder="Description">
        </div>
        
        <label>Projects</label>
        <div class="row">
            <input type="text" name="c_proj1" placeholder="Project Title">
            <input type="text" name="c_projdes1" placeholder="Description">
        </div>
        <div class="row">
            <input type="text" name="c_proj2" placeholder="Project Title">
            <input type="text" name="c_projdes2" placeholder="Description">
        </div>
        
        <label>Certificates</label>
        <div class="row">
            <input type="text" name="c_cert1" placeholder="Certificate Name">
            <input type="text" name="c_certdes1" placeholder="Description">
        </div>
        <div class="row">
            <input type="text" name="c_cert2" placeholder="Certificate Name">
            <input type="text" name="c_certdes2" placeholder="Description">
        </div>
        
        <button type='submit' id='res_gen_btn'>Generate & Download</button>
        </form>
    </div>
  `
  const res_gen_modal = document.getElementById('res_gen_feature');
  res_gen_modal.onclick = async function() {
    await openModal("Resume Generator",content,'35%');
    document.getElementById('resumeUserForm').addEventListener('submit',async function (params) {
      console.log('this is saem');
      params.preventDefault();
      const formData = new FormData(this);
      const jsonData = Object.fromEntries(formData.entries());
      aibtn = document.getElementById('res_gen_btn')
      aibtn.disabled = true
      aibtn.style.cursor = "not-allowed";
      aibtn.innerText = "Processing...";
      await fetch('/fsomewhere',{
        method:'POST',
        headers : {
          'Content-Type': 'application/json'
        },
        body:JSON.stringify(jsonData)
      }).then(response => response.json())
      .then(data => {
        console.log('status:',data);
        fetch(`/downloadresume?filepath=${data}`,{
          method:'GET',
          headers:{
            'Content-Type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
          }

        }).then(response =>{
          if (!response.ok) throw new Error("Download failed");
          return response.blob();
        }).then(blob => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = ''; // set filename
          document.body.appendChild(a);
          a.click();
          a.remove();
          window.URL.revokeObjectURL(url); // cleanup
        }).catch(err => console.error('Download error:', err));
    
        aibtn.disabled = false;
        aibtn.style.cursor = "pointer";
        aibtn.innerText = "Generate & Download";
      });
    
    });

  }
}

res_gen_ai();

async function checkvaultfiles(params) {
  try{

    let response = await fetch('/getvaultfiles');
    if (!response.ok){
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    data = await response.json();
    return data
  }
  catch(e){
    console.log(e);
    
  }
}

async function downloadanyfile(params) {
  fetch(`/downloadanyfile?filepath=${params}`, {
    method: 'GET'
  })
  .then(response => {
    if (!response.ok) throw new Error("Download failed");
  
    // Try to extract filename from headers
    const disposition = response.headers.get("Content-Disposition");
    // Extract the filename (without extension)
    const filenameMatch = disposition.match(/filename="([^"]+)"/);

    let filenameWithoutExtension = '';
    if (filenameMatch && filenameMatch[1]) {
      const filename = filenameMatch[1];
      filenameWithoutExtension = filename.replace(/\.[^/.]+$/, ''); // Remove extension
    }
  
    return response.blob().then(blob => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filenameWithoutExtension;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    });
  })
  .catch(err => console.error('Download error:', err));
  
}

async function removeanyfile(params) {
  await fetch(`/removeanyfile?filepath=${params}`, {
    method: 'GET'
  }).then(response =>{
    if (!response.ok){
      throw new Error("Error downloading file");
    }
  }).catch(err =>{
    alert("error",err);
  });

}

async function openingvault() {
  let vaultbtn = document.getElementById('openvault');
  let content = `<div class="uploadfile" id="uploadfile">
                    <input type="file" id="fileinput">
                    <button id="uploadBtn">UploadFile</button>
                </div>
                <div class="file-list"> </div>`;

  vaultbtn.onclick = async function() {
    // check how js reacts when it fetches no files i.e {}
    openModal('Vault',content,'60%','80%');
    let filesdata = await checkvaultfiles();
    let filelist = document.querySelector(".file-list");
        filelist.innerHTML = '';
        for (let key in filesdata){
          filelist.innerHTML += `<div class="file-item">
          <span class="file-name">${key}</span>
          <div class="file-actions">
            <span class="download-icon" data-value="${filesdata[key]}" >Download</span>
            <span class="delete-icon" data-value="${filesdata[key]}" >Delete.</span>
          </div>
        </div>`
        }

    const uploadBtn = document.getElementById("uploadBtn");
    const fileInput = document.getElementById("fileinput");
    uploadBtn.addEventListener('click',async () => {
      const file = fileInput.files[0];
      if(!file){
        alert("No file selected for upload");
        return;
      }

      if (file.size > 10 * 1024 * 1024) {
        alert("File too big! Max allowed size is 10MB.");
        return;
      }

      const formData = new FormData();
      formData.append('file',file);
      try {
        const response = await fetch('/uploadvault',
          {method:"POST",
          body: formData}
        );

        const result = await response.json();
        if(!response.ok){
          throw new Error(result.detail || "Upload failed");
        }
        console.log("Upload successful:", result);

        let files = await checkvaultfiles();
        filelist.innerHTML = '';
        for (let key in files){
          filelist.innerHTML += `<div class="file-item">
          <span class="file-name">${key}</span>
          <div class="file-actions">
            <span class="download-icon" data-value="${files[key]}">Download</span>
            <span class="delete-icon" data-value="${files[key]}">Delete.</span>
          </div>
        </div>`
        }

      } catch (error) {
        console.error(error);
      }
    });

    document.querySelectorAll('.download-icon').forEach(btn=>{
      btn.addEventListener('click',async ()=>{
        try {
          await downloadanyfile(btn.dataset.value);
        } catch (error) {
          console.log(error);
        }
      });
      
    });

    document.querySelectorAll(".delete-icon").forEach(btn =>{
      btn.addEventListener('click',async () => {
        try {
          await removeanyfile(btn.dataset.value);
          eleRemove = btn.parentElement.parentElement.remove();
        } catch (error) {
          console.log(error);
        }
      });
    });
  };

}
openingvault();


// modals
function openModal(title, content,width='',height='') {
    const overlay = document.getElementById('modalOverlay');
    const modalTitle = document.getElementById('modalTitle');
    const modalContent = document.getElementById('modalContent');
    const modelFrame=document.querySelector('.modal-frame');
    
    modalTitle.textContent = title;
    modalContent.innerHTML = content;
    overlay.style.display = 'flex';
    modelFrame.style.overflow = 'auto';
    if(width!=''){
      modelFrame.style.width=width;
    }
    if(height!=''){
      modelFrame.style.height=height;
    }
  }
  
function closeModal() {
  document.getElementById('modalOverlay').style.display = 'none';
}
  
  function openJobDetails(job) {
    // let job = JSON.parse(jobString)
    // Set the content dynamically
    document.getElementById('job-title').innerText = "Role: "+job.role;
    document.getElementById('job-company').innerText = "Company : "+job.company;
    document.getElementById('job-Postedby').innerText = "Posted-by: "+job.posted_by;
    document.getElementById('job-Postedon').innerText = "Posted-on: "+job.posted_on;
    document.getElementById('job-skills').innerText = "Skills Required : "+job.skills;
    document.getElementById('job-batch').innerText = "Elgible-batch : "+job.batch;
    document.getElementById('job-dept').innerText = "Elgible-Domain : "+job.department_req;
    document.getElementById('job-sem').innerText = "Semester-Completed : "+job.sem_completed;
    document.getElementById('job-cgpa').innerText = "CGPA-req : "+job.cgpa_value+'+';
    document.getElementById('job-applyby').innerText = "Apply-by : "+job.apply_by;
    document.getElementById('job-description').innerText = "Description : "+job.description;
    document.getElementById('job-applylink').href= job.apply_link;

    // Show the frame
    document.getElementById('job-detail-frame').classList.add('active');
    document.body.classList.add('modal-open'); // Blur background
}

function closeJobDetails() {
    document.getElementById('job-detail-frame').classList.remove('active');
    document.body.classList.remove('modal-open');
}

  