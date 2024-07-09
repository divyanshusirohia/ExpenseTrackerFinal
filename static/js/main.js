document.addEventListener("DOMContentLoaded", function () {
  // Fetch expenses data and update chart
  fetch("/api/expenses")
    .then((response) => response.json())
    .then((data) => {
      updateChart(data);
    });

  function updateChart(expenses) {
    const ctx = document.getElementById("expenseChart").getContext("2d");

    // Process data for the chart
    const labels = expenses.map((expense) => expense.expense);
    const amounts = expenses.map((expense) => expense.amount);

    new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Expense Amount",
            data: amounts,
            backgroundColor: "rgba(54, 162, 235, 0.6)",
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  }
});
