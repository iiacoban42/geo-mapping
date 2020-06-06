describe('Tiles Overview', function () {
    it('is working', () => {
        cy.visit('/tiles_overview');
    });

    it('has working nav menu', () => {
        cy.visit('/tiles_overview');
        cy.get('#myNav').should('be.not.visible');
        cy.get('.open').click();
        cy.get('#myNav').should('be.visible');

        cy.get('#maps').click()
        cy.url().should('eq', 'http://127.0.0.1:8000/')

        cy.visit('/tiles_overview');
        cy.get('.open').click();

        cy.get('#captcha').click()
        cy.url().should('eq', 'http://127.0.0.1:8000/captca')
    })
})