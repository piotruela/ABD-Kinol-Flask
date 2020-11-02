let final_element_dimension_px = 40;
let final_margin_px = 3;

function createRoomSitsView(room_columns, room_rows, hover) {
    const room_columns_with_pre_column = parseInt(room_columns) + 1
    const max_element_dimension_px = 40
    const element_dimension_px = Math.min((window.innerWidth * 2 / room_columns_with_pre_column) - (room_columns_with_pre_column * final_margin_px), max_element_dimension_px)
    final_element_dimension_px = element_dimension_px
    const grid_container = document.getElementById("room-grid-container")
    while (grid_container.firstChild) {
        grid_container.removeChild(grid_container.lastChild);
    }
    grid_container.style.gridTemplateColumns = `repeat(${room_columns_with_pre_column}, 1fr)`
    grid_container.style.width = `${(element_dimension_px + final_margin_px) * room_columns_with_pre_column}px`
    while (parent.firstChild) {
        parent.firstChild.remove()
    }


    for (let row = 0; row < room_rows; row++) {
        const pre_row_grid_element = createBaseGridRoomElement(row + 1, 0, element_dimension_px)
        pre_row_grid_element.innerText = `no. ${row + 1}`
        pre_row_grid_element.id = `room-grid-row-iterator-${row}`
        grid_container.appendChild(pre_row_grid_element)
        for (let column = 0; column < room_columns; column++) {
            const room_grid_element = createBaseGridRoomElement(row + 1, column + 1)
            if (hover === true) {
                addDecoratedRoomElementSitHover(room_grid_element)
            }
            room_grid_element.sitIterator = `${column + 1}`
            grid_container.appendChild(room_grid_element)
            room_grid_element.row = row
            room_grid_element.column = column
        }
    }
}

function createBaseGridRoomElement(row, column, element_dimension_px) {
    const room_grid_element = document.createElement('div')
    room_grid_element.innerText = ''
    room_grid_element.style.width = `${element_dimension_px}px`
    room_grid_element.style.height = `${element_dimension_px}px`
    room_grid_element.style.margin = `${final_margin_px}px`
    room_grid_element.id = `room-grid-container-element-${row}-${column}`
    return room_grid_element
}

function decoratedGridRoomOnMouseOver(room_grid_element) {
    room_grid_element.style.backgroundColor = "white"
    room_grid_element.style.color = "black"
}

function decoratedGridRoomOnMouseOut(room_grid_element) {
    if (room_grid_element.not_hover_out_background_color) {
        room_grid_element.style.backgroundColor = room_grid_element.not_hover_out_background_color
    } else {
        room_grid_element.style.backgroundColor = "#363636"
    }
    if (room_grid_element.not_hover_out_color) {
        room_grid_element.style.color = room_grid_element.not_hover_out_color
    } else {
        room_grid_element.style.color = "white"
    }
}

function addDecoratedRoomElementSitHover(room_grid_element) {
    room_grid_element.onmouseover = function () {
        decoratedGridRoomOnMouseOver(room_grid_element)
    }
    room_grid_element.onmouseout = function () {
        decoratedGridRoomOnMouseOut(room_grid_element)
    }
}

function decorateGridRoomElementSit(room_grid_element) {
    room_grid_element.style.backgroundColor = "#363636"
    room_grid_element.style.border = "1px solid blue"
    room_grid_element.style.color = "white"
    room_grid_element.innerText = room_grid_element.sitIterator
    room_grid_element.decorated = true
}

function notDecoratedGridRoomOnMouseOver(room_grid_element) {
    room_grid_element.style.backgroundColor = "#363636"
    room_grid_element.style.color = "white"
}

function notDecoratedGridRoomOnMouseOut(room_grid_element) {
    room_grid_element.style.backgroundColor = "white"
    room_grid_element.style.color = "black"
}

function removeDecoratedGridRoomElementSitHover(room_grid_element) {
    room_grid_element.onmouseover = function () {
        notDecoratedGridRoomOnMouseOver(room_grid_element)
    }
    room_grid_element.onmouseout = function () {
        notDecoratedGridRoomOnMouseOut(room_grid_element)
    }
}

function removeDecorationGridRoomElementSit(room_grid_element) {
    room_grid_element.style.backgroundColor = "white"
    room_grid_element.style.color = "black"
    room_grid_element.innerText = room_grid_element.sitIterator
    room_grid_element.decorated = false
}