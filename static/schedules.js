document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#course').onchange = () => {

        // Initialize new request
        const request = new XMLHttpRequest();
        const course_id = document.querySelector('#course').value;
        request.open('GET', `/courses/${course_id}`);

        // Callback function for when request completes
        request.onload = () => {

            // Extract JSON data from request
            console.log(request.responseText);
            const data = JSON.parse(request.responseText);

            // Update the result div
            if (request.status == 200) {
                document.querySelector('#list-info').style.display = ''
                document.querySelector('#list-name').innerHTML = `Name: ${data.name}`;
                document.querySelector('#list-semester').innerHTML = `Semester: ${data.semester}`;
                document.querySelector('#list-category').innerHTML = `Category: ${data.category}`;
                document.querySelector('#list-credits').innerHTML = `Credits: ${data.credits}`;
            }
            else {
                document.querySelector('#result').innerHTML = 'There was an error.';
            }
        }

        // Send request
        request.send();
        return false;
    };

});
