
function toggleComments(id) {
    let comments = document.querySelectorAll('.comment-none')
    console.log(comments)
    comments.forEach(node => {
        
        if (node.id == id){
            console.log(node)
            if (node.classList.contains('comment-none')) {
                node.classList.remove('comment-none')
            }else {
                node.classList.add('comment-none')

            }
        }
    
    });
}
