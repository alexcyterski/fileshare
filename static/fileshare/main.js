document.addEventListener('DOMContentLoaded', function() {

    // mouseover highlighting
    addFileHoverListeners();
    addDeleteHoverListeners();

    // handle upload button click
    const forms = document.forms
    document.getElementById('upload-link').addEventListener('click', () => {
        document.getElementById('file-input').click();
    })

    document.getElementById('file-input').addEventListener('change', () => {
        forms[0].submit();
    })

})

function addFileHoverListeners() {
    const upload_link = document.querySelector('#upload-link')
    const upload_row = document.querySelector('.upload-row')
    const row_list = document.querySelectorAll('.file-name')

    row_list.forEach(item => {
        let file_row_div = item.parentElement.parentElement.parentElement;
        item.addEventListener('mouseover', () => {
            file_row_div.style.backgroundColor = 'rgb(230, 230, 230)';
            item.style.textDecoration = 'underline';
        })
        item.addEventListener('mouseout', () => {
            file_row_div.style.backgroundColor = '';
            item.style.textDecoration = 'none';
        })
    });

    upload_link.addEventListener('mouseover', () => {
        upload_row.style.backgroundColor = 'rgb(230, 230, 230)';
        upload_link.style.backgroundColor = 'rgb(230, 230, 230)';
        upload_link.style.textDecoration = 'underline';
    });
    upload_link.addEventListener('mouseout', () => {
        upload_row.style.backgroundColor = '';
        upload_link.style.backgroundColor = '';
        upload_link.style.textDecoration = 'none';
    });

}

function addDeleteHoverListeners() {
    const delete_button_list = document.querySelectorAll('.delete')

    delete_button_list.forEach(item => {
        item.firstElementChild.addEventListener('mouseover', () => {
            item.style.backgroundColor = 'rgb(230, 230, 230)';
            item.firstElementChild.style.backgroundColor = 'rgb(230, 230, 230)';
            item.firstElementChild.style.textDecoration = 'underline';
        })
        item.firstElementChild.addEventListener('mouseout', () => {
            item.style.backgroundColor = '';
            item.firstElementChild.style.backgroundColor = '';
            item.firstElementChild.style.textDecoration = 'none';
        })
    })
}