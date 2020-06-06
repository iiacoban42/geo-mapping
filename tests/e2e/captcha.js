describe('Captcha', function () {
    it('is working correctly', () => {
        cy.visit('/captcha');

        cy.get('#checkmark').click();
        cy.get('#water1').click();
        cy.get('#building1').click();
        cy.get('#nextChallenge').click();

        cy.get('#water2').click();
        cy.get('#building2').click();
        cy.get('#submit').click();
    });

    it('has working info with legend', () => {
        cy.visit('/captcha');

        // Should be not visible before mouseover
        cy.get('#legend_info').should('be.not.visible');
        cy.get('#legend_btn').trigger('mouseover');

        // Should be visible after mouseover
        cy.get('#legend_info').should('be.visible');
    })

    it('has working nav menu', () => {
        cy.visit('/captcha');

        cy.get('#myNav').should('be.not.visible');
        cy.get('.open').click();
        cy.get('#myNav').should('be.visible');

        cy.get('#maps').click()
        cy.url().should('eq', 'http://127.0.0.1:8000/')

        cy.visit('/captcha');
        cy.get('.open').click();

        cy.get('#tiles_overview').click()
        cy.url().should('eq', 'http://127.0.0.1:8000/tiles_overview')
    })
})