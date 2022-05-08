/// <reference types="cypress" />

describe('Logging into the system', () => {
    var secondTest = false;
    beforeEach(function() {
        // create a fabricated user from a fixture
        cy.visit("http://localhost:3000/")
        cy.fixture('user.json')
        .then((user) => {
            cy.request({
                method: 'POST',
                url: 'http://localhost:5000/users/create',
                    form: true,
                    body: user
                }).then((response) => {
                    this.uid = response.body._id.$oid

                    // create one fabricated task for that user
                    cy.fixture('task.json')
                    .then((task) => {
                            // add the user id to the data of the task object
                            task.userid = this.uid
                            cy.request({
                                method: 'POST',
                                url: 'http://localhost:5000/tasks/create',
                                form: true,
                                body: task
                            }).then((response) => {
                                this.tid = response.body[0]._id.$oid

                                cy.fixture('todo.json').then((todo) => {
                                    // add the task id to the data of the todo object
                                    todo.taskid = this.tid
                                    if (secondTest) {
                                        todo.done = true
                                    }
                                    cy.request({
                                        method: 'POST',
                                        url: 'http://localhost:5000/todos/create',
                                        form: true,
                                        body: todo
                                    }).then((response) => {
                                        this.toid = response.body
                                    })
                                })
                            })
                        })
                })
            })
            cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type('mon.doe@gmail.com')
            // alternative, imperative way of detecting that input field
            /*cy.get('.inputwrapper #email')
                .type('mon.doe@gmail.com')*/

            // submit the form on this page
            cy.get('form')
                .submit()

            cy.get('img')
                .click()

    })


    it('check todo', () => {
        // find span and click it
        cy.get('.todo-list').find('li').eq(1).find('span').first().click()
        cy.get('.todo-list').find('li').eq(1).find('span').first().should('have.class', 'checker checked')

        // Hade varit bättre att lösa detta på annat sätt
        secondTest = true;
    })

    it('uncheck todo', () => {

        cy.get('.todo-list').find('li').eq(1).find('span').first().click()
        cy.get('.todo-list').find('li').eq(1).find('span').first().should('have.class', 'checker unchecked')

    })

    afterEach(function() {
        // clean up by deleting the user from the database
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${this.uid}`
        }).then((response) => {
            cy.log(response.body)
        })
    })
})