<template>
    <div class="plagiarism-check-container">
        <div class="header">
            <h1>Plagiarism Check</h1>
        </div>

        <div class="input-section">
            <input v-model="githubRepoLink" type="text" placeholder="Enter GitHub Repository Link" class="repo-input" />
            <input v-model="studentName" type="text" placeholder="Enter Student/Team Name" class="name-input" />
            <button @click="checkPlagiarism" class="check-btn">
                Check Plagiarism
            </button>
        </div>

        <div v-if="score !== null" class="score-card">
            <div class="score-circle">{{ score.toFixed(2) }}%</div>
            <div class="score-label">Overall Similarity Score</div>
        </div>

        <div v-if="plagiarismResults.length > 0" class="results-table">
            <table>
                <thead>
                    <tr>
                        <th>Student Name</th>
                        <th>Repository Link</th>
                        <th>Plagiarism Score</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(result, index) in plagiarismResults" :key="index">
                        <td>{{ result.student_name }}</td>
                        <td><a :href="result.repo_link" target="_blank">{{ result.repo_link }}</a></td>
                        <td>{{ result.score.toFixed(2) }}%</td>
                        <td :class="result.status">{{ result.status.toUpperCase() }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            githubRepoLink: '',
            studentName: '',
            score: null,
            plagiarismResults: [],
        };
    },
    methods: {
        async checkPlagiarism() {
            if (!this.githubRepoLink || !this.studentName) {
                alert('Please provide both the GitHub repository link and the student name.');
                return;
            }

            try {
                const response = await axios.post('/api/check_plagiarism', {
                    github_repo_link: this.githubRepoLink,
                    student_name: this.studentName,
                }, {
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });

                const { overall_score, plagiarism_results } = response.data;
                this.score = overall_score;
                this.plagiarismResults = plagiarism_results;
            } catch (error) {
                console.error('Error checking plagiarism:', error);
                alert('An error occurred while checking plagiarism. Please ensure the GitHub link is correct and try again.');
            }
        },
    },
};
</script>

<style scoped>
.plagiarism-check-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 30px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.header {
    text-align: center;
    margin-bottom: 30px;
}

.header h1 {
    color: #333;
    font-size: 2.5em;
}

.input-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
}

.repo-input,
.name-input {
    width: 100%;
    max-width: 600px;
    padding: 12px 20px;
    border: 2px solid #ccc;
    border-radius: 5px;
    font-size: 1em;
    transition: border-color 0.3s;
}

.repo-input:focus,
.name-input:focus {
    border-color: #4CAF50;
    outline: none;
}

.check-btn {
    padding: 12px 25px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 1em;
    cursor: pointer;
    transition: background-color 0.3s;
}

.check-btn:hover {
    background-color: #45a049;
}

.score-card {
    margin-top: 30px;
    text-align: center;
}

.score-circle {
    width: 120px;
    height: 120px;
    margin: 0 auto;
    border-radius: 50%;
    background: conic-gradient(#4CAF50 0% 0%, #f0f0f0 0%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5em;
    color: #333;
    position: relative;
}

.score-label {
    margin-top: 10px;
    font-size: 1.2em;
    color: #555;
}

.score-circle::after {
    content: '';
    position: absolute;
    width: 90%;
    height: 90%;
    background-color: #f9f9f9;
    border-radius: 50%;
}

.results-table {
    margin-top: 40px;
    overflow-x: auto;
}

.results-table table {
    width: 100%;
    border-collapse: collapse;
    background-color: white;
}

.results-table th,
.results-table td {
    padding: 12px 15px;
    border: 1px solid #ddd;
    text-align: center;
}

.results-table th {
    background-color: #4CAF50;
    color: white;
    font-size: 1em;
}

.results-table tr:nth-child(even) {
    background-color: #f2f2f2;
}

.pass {
    color: green;
    font-weight: bold;
}

.fail {
    color: red;
    font-weight: bold;
}

a {
    color: #4CAF50;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}
</style>
