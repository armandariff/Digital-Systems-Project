
// Function to show menu bar
function toggleDisplay(id, ev='Not form eventlistner'){
    let element = document.getElementById(id)

    if (element.style.display === 'none') {
        element.style.display = 'block';
    } else {
        element.style.display = 'none';
    }
}