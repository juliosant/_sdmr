let tags = []
let tagContainer = document.querySelector('.tagContainer')
//let input = tagContainer.querySelector('input')
let input = document.querySelector('#inputTag')

input.addEventListener('keyup', addTags)

input.addEventListener('keyup', function(e){
    if(e.keyCode === '13'){
        console.log('passou')
    }
})

function addTags(event){
    const keyPressedIsEnter = event.keyCode == '13'
    if(keyPressedIsEnter){
        input.value.split(',').forEach( tag =>{
            if(tag){
                tags.push(tag.trim())
            }
        })
        updateTags()
        input.value = ""
    }
}

function updateTags(){
    clearTags()
    tags.slice().reverse().forEach(tag => {
        tagContainer.prepend(createTag(tag))
    })
}

function createTag(tag){
    const div = document.createElement('div')
    div.classList.add('bg-success')
    div.classList.add('rounded')
    div. classList.add('tag')

    const span = document.createElement('span')
    span.innerHTML = tag
    div.append(span)

    const i = document.createElement('i')
    i.classList.add('close')
    i.setAttribute('data-id', tag)
    i.onclick = removeTag
    span.append(i)

    return div
}

function removeTag(event){
    const buttonX = event.currentTarget
    const id = buttonX.dataset.id
    const index = tags.indexOf(id)
    tags.splice(index, 1)

    updateTags()
}

function clearTags(){
    tagContainer.querySelectorAll('.tag').forEach(tagElements => tagElements.remove())
}


function receiveTags(){
    let receiver = document.querySelector('#receiverTags')
    //console.log(receiver.value)
    receiver.value = tags.join()
    console.log(receiver.value)
}

// jquery
$(window).ready(function() {
    $("#formTag").on("keypress", function (event) {
        //console.log("aaya");
        var keyPressed = event.keyCode || event.which;
        if (keyPressed === 13) {
            //alert("You pressed the Enter key!!");
            event.preventDefault();
            return false;
        }
    });
    });

    $(window).ready(function() {
        $("#buttonRegisterRC").on("click", function (event) {
            //console.log("aaya");
            var keyPressed = event.keyCode || event.which;
            if (tags.length === 0) {
                alert("Adicione pelo menos 1 material!!");
                event.preventDefault();
                return false;
            }
        });
    });