import Swal from "sweetalert2";

export const successMessage = function(msg){
    Swal.fire({
    position: "top-end",
    icon: "success",
    title: msg || "Success",
    showConfirmButton: false,
    timer: 1500
    });
}

export const failedMessage = function(msg){
    Swal.fire({
    position: "top-end",
    icon: "error",
    title: msg || "Something went wrong, please try again later",
    showConfirmButton: false,
    timer: 1500
    });
}
