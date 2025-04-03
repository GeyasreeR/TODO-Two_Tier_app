document.addEventListener("DOMContentLoaded", () => {
    const checkboxes = document.querySelectorAll(".todo-check");
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener("change", async () => {
            const todoItem = checkbox.closest(".todo-item");
            const todoId = todoItem.dataset.id;
            const completed = checkbox.checked;
            const text = todoItem.querySelector(".todo-text");

            // Update server
            await fetch(`/todos/${todoId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ completed })
            });

            // Update UI
            text.classList.toggle("completed", completed);
        });
    });

    // Fade-in animation
    const items = document.querySelectorAll(".todo-item");
    items.forEach((item, index) => {
        setTimeout(() => {
            item.style.opacity = "1";
        }, index * 100);
    });
});