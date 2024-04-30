function iks() {
    const cancel = document.querySelector('.iks')
    const added = document.querySelector('.plused')
    const madalni = document.querySelector('.madalni')

    cancel.addEventListener('click', () => {
        madalni.style.visibility = `hidden`
    })
    added.addEventListener('click', () => {
        madalni.style.visibility = `visible`
    })


}

iks()
const cancel2 = document.querySelectorAll('.mad .iks2')
const edit = document.querySelectorAll('.edit')
const madalni2 = document.querySelector('.madalni2')
cancel2.forEach((item, id) => {
    item.addEventListener('click', () => {
        madalni2.style.visibility = `hidden`
    })
})
edit.forEach((item, id) => {
    item.addEventListener('click', () => {
        madalni2.style.visibility = `visible`
    })
})