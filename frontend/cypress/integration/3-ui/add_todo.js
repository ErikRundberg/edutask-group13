/// <reference types="cypress" />

describe('Logging into the system', () => {
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
                                this.tid = response.body
                            })
                        })
                })
            })
            // detect a div which contains "Email Address", find the input and type
            // declarative
            cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type('mon.doe@gmail.com')
            // alternative, imperative way of detecting that input field
            /*cy.get('.inputwrapper #email')
                .type('mon.doe@gmail.com')*/

            // submit the form on this page
            cy.get('form')
                .submit()

            // assert that the user is now logged in
            cy.get('img')
                .click()
    })


    it('create new todo', () => {

        cy.get('.todo-list').get(".inline-form").type("Take notes")
        
        cy.get('.todo-list').get(".inline-form").find('input[type=submit]').click()

        cy.get('.todo-list').children().its('length').should('eq', 3)
        cy.get('.todo-list').find('li').eq(1).find('span').eq(1).should('contain.text', 'Take notes')

        // cy.get('.todo-list').should('have.length', 2)

    })

    it("failed to create todo", () => {
        cy.viewport(1920, 1080)

        cy.get('.todo-list').get(".inline-form").find('input[type=submit]').click({force: true})

        cy.get('.todo-list').get(".inline-form").find('input[type=submit]').should('have.css', 'border-color', 'red')
        cy.get('.todo-list').children().its('length').should('eq', 2)
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