// Selecting all sections with class of section
const sections = document.querySelectorAll('.section')
  
// On click event for each section 
sections.forEach((section)=>{
section.addEventListener('click',()=>{
    // remove active class from all another section 
    // and add it to the selected section
    sections.forEach((section) => {
        section.classList.remove('active')
    })
    section.classList.add('active')
})
})