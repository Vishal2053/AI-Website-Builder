
        document.addEventListener('DOMContentLoaded', function() {
            const qc1Btn = document.getElementById('qc1Btn');
            const qc2Btn = document.getElementById('qc2Btn');
            const qc1Table = document.getElementById('qc1Table');
            const qc2Table = document.getElementById('qc2Table');
            const markQc1Links = document.querySelectorAll('.markQc1');
            const qc1Rows = qc1Table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');

            qc1Btn.addEventListener('click', () => {
                qc1Table.classList.remove('hidden');
                qc2Table.classList.add('hidden');
            });

            qc2Btn.addEventListener('click', () => {
                qc2Table.classList.remove('hidden');
                qc1Table.classList.add('hidden');
                updateQc2Table();
            });

            markQc1Links.forEach(link => {
                link.addEventListener('click', function(event) {
                    event.preventDefault();
                    const row = this.closest('tr');
                    const qc1Status = row.querySelector('.qc1Status');
                    if (qc1Status.textContent === '') {
                        qc1Status.textContent = '✓';
                        qc1Status.classList.add('checkmark');
                        row.style.display = 'none';
                        updateQc2Table();
                    } else {
                        qc1Status.textContent = '';
                        qc1Status.classList.remove('checkmark');
                        row.style.display = '';
                        updateQc2Table();
                    }
                });
            });

            function updateQc2Table() {
                const qc2Tbody = qc2Table.getElementsByTagName('tbody')[0];
                qc2Tbody.innerHTML = '';
                for (let row of qc1Rows) {
                    const qc1Status = row.querySelector('.qc1Status').textContent;
                    if (qc1Status === '✓') {
                        const newRow = qc2Tbody.insertRow();
                        newRow.insertCell(0).innerHTML = '<span class="qc2Status"></span>';
                        for (let i = 1; i < row.cells.length - 1; i++) {
                            newRow.insertCell(i).textContent = row.cells[i].textContent;
                        }
                        const buttonsCell = newRow.insertCell(row.cells.length - 1);
                        const link = document.createElement('a');
                        link.href = '#';
                        link.innerHTML = '<i class="fas fa-link"></i>';
                        link.addEventListener('click', function(event) {
                            event.preventDefault();
                            const qc2Status = newRow.querySelector('.qc2Status');
                            if (qc2Status.textContent === '') {
                                qc2Status.textContent = '✓';
                                qc2Status.classList.add('checkmark');
                            } else {
                                qc2Status.textContent = '';
                                qc2Status.classList.remove('checkmark');
                            }
                        });
                        buttonsCell.appendChild(link);
                    }
                }
            }
        });
    