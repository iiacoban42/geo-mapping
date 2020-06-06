describe('Tiles Overview', function () {
    it.only('updates numbers when selecting a year', () => {
        cy.visit('/tiles_overview');
        // Check if number of dataset tiles appears after selecting a year
        cy.get('#dataset_year').invoke('text').then((textBefore) => {
            cy.get('select').select('2016');
            cy.wait(1000);
            cy.get('#dataset_year').invoke('text').then((textAfter) => {
                expect(textBefore).not.equal(textAfter);
            });
        });
    });

    it('has working nav menu', () => {
        cy.visit('/tiles_overview');
        cy.get('#myNav').should('be.not.visible');
        cy.get('.open').click();
        cy.get('#myNav').should('be.visible');

        cy.get('#maps').click();
        cy.url().should('eq', 'http://127.0.0.1:8000/');

        cy.visit('/tiles_overview');
        cy.get('.open').click();

        cy.get('#captcha').click();
        cy.url().should('eq', 'http://127.0.0.1:8000/captcha');
    })
});